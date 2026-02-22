#!/usr/bin/env python3
"""Week 2 scaffold: alias application, target inference, and v1 edge/node outputs.

This is a starter pipeline intended for iterative refinement.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys


try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "This scaffold requires pandas in your runtime. "
        "Use your notebook kernel/venv where Week 1 ran."
    ) from exc


ATTACK_TERMS = {
    "failed",
    "failure",
    "dangerous",
    "corrupt",
    "lies",
    "lying",
    "radical",
    "extreme",
    "crime",
    "criminal",
    "inflation",
    "border",
    "illegal",
    "tax",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Week 2 attack-target v1 outputs.")
    parser.add_argument(
        "--mentions",
        default="outputs/week1/entity_mentions_week1.parquet",
        help="Path to Week 1 mentions artifact (parquet preferred).",
    )
    parser.add_argument(
        "--aliases",
        default="outputs/week1/entity_alias_map_v1.csv",
        help="Path to reviewed alias map.",
    )
    parser.add_argument(
        "--out-dir",
        default="outputs/week2",
        help="Output directory for edge/node artifacts.",
    )
    return parser.parse_args()


def detect_analysis_root() -> Path:
    """Find project root so relative paths work from any cwd."""
    cwd = Path.cwd().resolve()
    script_dir = Path(__file__).resolve().parent
    candidates = [cwd, script_dir, script_dir.parent, cwd.parent]

    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "data").exists():
            return candidate

    return cwd


def resolve_path(path_str: str, analysis_root: Path) -> Path:
    path = Path(path_str).expanduser()
    if path.is_absolute():
        return path
    return (analysis_root / path).resolve()


def read_mentions(path: Path, analysis_root: Path) -> pd.DataFrame:
    if path.suffix == ".parquet" and path.exists():
        return pd.read_parquet(path)

    if path.exists():
        return pd.read_csv(path)

    fallback = (analysis_root / "outputs" / "week1" / "entity_mentions_week1.csv.gz").resolve()
    if fallback.exists():
        return pd.read_csv(fallback, compression="gzip")

    raise FileNotFoundError(
        f"Mentions file not found: {path}\n"
        f"Checked fallback: {fallback}\n"
        f"cwd={Path.cwd().resolve()} analysis_root={analysis_root}"
    )


def normalize_text(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_for_match(s: str) -> str:
    s = normalize_text(s)
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_alias_map(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Alias map not found: {path}. "
            "Create/review outputs/week1/entity_alias_map_v1.csv first."
        )

    alias = pd.read_csv(path)
    required = {"entity_text", "entity_label", "canonical_final"}
    missing = required - set(alias.columns)
    if missing:
        raise ValueError(f"Alias map missing required columns: {sorted(missing)}")

    alias = alias.copy()
    alias["entity_text_norm"] = alias["entity_text"].map(normalize_for_match)
    alias["canonical_final"] = alias["canonical_final"].fillna("").astype(str).str.strip()
    alias["review_status"] = alias.get("review_status", "PENDING").fillna("PENDING")
    alias = alias.drop_duplicates(subset=["entity_text_norm", "entity_label"], keep="first")
    return alias


def apply_aliases(mentions: pd.DataFrame, alias: pd.DataFrame) -> pd.DataFrame:
    df = mentions.copy()
    df["entity_text_norm"] = df["entity_text"].map(normalize_for_match)
    merged = df.merge(
        alias[["entity_text_norm", "entity_label", "canonical_final", "review_status"]],
        on=["entity_text_norm", "entity_label"],
        how="left",
    )
    merged["canonical_entity"] = merged["canonical_final"].where(
        merged["canonical_final"].fillna("").str.len() > 0, merged["entity_text_norm"]
    )
    merged["alias_review_status"] = merged["review_status"].fillna("UNMAPPED")
    return merged


def mark_target_signals(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["tone_std"] = out["tone_std"].fillna("UNKNOWN")
    out["negative_tone"] = out["tone_std"].isin(["NEGATIVE", "CONTRAST"])
    out["context_window"] = out["context_window"].fillna("").astype(str)
    out["context_has_attack_term"] = out["context_window"].str.lower().map(
        lambda t: any(term in t for term in ATTACK_TERMS)
    )

    sponsor_norm = out["sponsor_name"].fillna("").map(normalize_for_match)
    canonical_norm = out["canonical_entity"].fillna("").map(normalize_for_match)
    # Row-wise check because pandas .str.contains does not accept a Series pattern.
    out["not_self_mention"] = [
        not (canon and canon in sponsor)
        for sponsor, canon in zip(sponsor_norm, canonical_norm)
    ]

    high = out["not_self_mention"] & out["negative_tone"] & out["context_has_attack_term"]
    medium = out["not_self_mention"] & (out["negative_tone"] | out["context_has_attack_term"]) & ~high
    low = ~high & ~medium

    out["target_confidence"] = "low"
    out.loc[medium, "target_confidence"] = "medium"
    out.loc[high, "target_confidence"] = "high"
    out["is_target"] = out["target_confidence"].isin(["high", "medium"])
    return out


def build_edges(df: pd.DataFrame) -> pd.DataFrame:
    target = df[df["is_target"]].copy()
    grouped = (
        target.groupby(["sponsor_name", "canonical_entity"], as_index=False)
        .agg(
            mention_count=("ad_id", "count"),
            ad_count=("ad_id", "nunique"),
            high_confidence_mentions=("target_confidence", lambda s: (s == "high").sum()),
            medium_confidence_mentions=("target_confidence", lambda s: (s == "medium").sum()),
            platform_count=("platform", "nunique"),
            party_mode=("party_std", lambda s: s.mode().iloc[0] if not s.mode().empty else "UNKNOWN"),
            tone_mode=("tone_std", lambda s: s.mode().iloc[0] if not s.mode().empty else "UNKNOWN"),
        )
        .sort_values("mention_count", ascending=False)
    )
    grouped["edge_confidence"] = grouped.apply(
        lambda r: "high"
        if r["high_confidence_mentions"] >= max(3, 0.5 * r["mention_count"])
        else "medium",
        axis=1,
    )
    return grouped


def build_nodes(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("canonical_entity", as_index=False)
        .agg(
            mention_count=("ad_id", "count"),
            ad_count=("ad_id", "nunique"),
            sponsor_count=("sponsor_name", "nunique"),
            platform_count=("platform", "nunique"),
            label_mode=("entity_label", lambda s: s.mode().iloc[0] if not s.mode().empty else "UNKNOWN"),
            high_confidence_mentions=("target_confidence", lambda s: (s == "high").sum()),
            medium_confidence_mentions=("target_confidence", lambda s: (s == "medium").sum()),
            low_confidence_mentions=("target_confidence", lambda s: (s == "low").sum()),
        )
        .sort_values("mention_count", ascending=False)
    )
    return grouped


def main() -> int:
    args = parse_args()
    analysis_root = detect_analysis_root()
    mentions_path = resolve_path(args.mentions, analysis_root)
    aliases_path = resolve_path(args.aliases, analysis_root)
    out_dir = resolve_path(args.out_dir, analysis_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"analysis_root: {analysis_root}")
    print(f"mentions_path: {mentions_path}")
    print(f"aliases_path: {aliases_path}")
    print(f"out_dir: {out_dir}")

    mentions = read_mentions(mentions_path, analysis_root)
    alias = load_alias_map(aliases_path)

    mentions = apply_aliases(mentions, alias)
    mentions = mark_target_signals(mentions)

    edges = build_edges(mentions)
    nodes = build_nodes(mentions)

    edge_path = out_dir / "attack_target_edges_v1.csv"
    node_path = out_dir / "attack_target_nodes_v1.csv"
    mentions_path = out_dir / "entity_mentions_week2_labeled_v1.csv.gz"

    edges.to_csv(edge_path, index=False)
    nodes.to_csv(node_path, index=False)
    mentions.to_csv(mentions_path, index=False, compression="gzip")

    print(f"Mentions in: {len(mentions):,}")
    print(f"Target mentions: {int(mentions['is_target'].sum()):,}")
    print(f"Edges out: {len(edges):,} -> {edge_path}")
    print(f"Nodes out: {len(nodes):,} -> {node_path}")
    print(f"Labeled mentions out: {mentions_path}")
    print("Scaffold complete. Review heuristics before final analysis.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
