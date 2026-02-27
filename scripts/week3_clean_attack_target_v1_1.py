#!/usr/bin/env python3
"""Week 3 conservative cleaning pipeline for attack-target graph v1.1."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit("This script requires pandas. Run from the analysis Poetry environment.") from exc


GENERIC_STOPLIST = {
    "vote",
    "votes",
    "voting",
    "senate",
    "congress",
    "america",
    "country",
    "state",
    "states",
    "people",
    "children",
    "taxpayer",
    "taxpayers",
}

ORG_SUFFIX_ONLY = {"pac", "inc", "llc", "committee"}
TARGET_TONES = {"NEGATIVE", "CONTRAST"}
TARGET_LABELS = {"PERSON", "ORG"}
BUILD_VERSION = "v1.1_conservative"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build conservative cleaned attack-target v1.1 artifacts.")
    parser.add_argument(
        "--mentions-in",
        default="outputs/week2/entity_mentions_week2_labeled_v1.csv.gz",
        help="Path to Week 2 mention table.",
    )
    parser.add_argument(
        "--aliases-in",
        default="outputs/week1/entity_alias_map_v1.csv",
        help="Path to reviewed alias map.",
    )
    parser.add_argument(
        "--out-dir",
        default="outputs/week3",
        help="Output directory for Week 3 cleaned artifacts.",
    )
    return parser.parse_args()


def detect_analysis_root() -> Path:
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


def normalize_for_match(value: object) -> str:
    s = "" if pd.isna(value) else str(value)
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_alias_map(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Alias map not found: {path}")

    alias = pd.read_csv(path)
    required = {"entity_text", "entity_label", "canonical_final"}
    missing = required - set(alias.columns)
    if missing:
        raise ValueError(f"Alias map missing required columns: {sorted(missing)}")

    alias = alias.copy()
    alias["entity_text_norm"] = alias["entity_text"].map(normalize_for_match)
    alias["canonical_final_norm"] = alias["canonical_final"].map(normalize_for_match)
    alias["review_status"] = alias.get("review_status", "PENDING").fillna("PENDING").astype(str).str.strip()
    alias = alias.drop_duplicates(subset=["entity_text_norm", "entity_label"], keep="first")
    return alias


def load_mentions(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Mentions input not found: {path}")
    return pd.read_csv(path, compression="gzip" if path.suffix == ".gz" else None)


def top_targets_string(series: pd.Series, n: int = 25) -> str:
    vc = series.value_counts().head(n)
    if vc.empty:
        return ""
    return "|".join([f"{idx}:{int(count)}" for idx, count in vc.items()])


def add_metric(metrics: list[dict[str, object]], stage: str, metric: str, value: object) -> None:
    metrics.append({"stage": stage, "metric": metric, "value": value})


def classify_initial_drop_reason(df: pd.DataFrame) -> pd.Series:
    canon = df["canonical_entity_v1_1"].fillna("")
    token_count = canon.str.split().map(len)
    is_empty = canon.eq("")
    is_numeric = canon.str.fullmatch(r"\d+")
    is_too_short = canon.str.len() <= 2
    is_single_person = (df["entity_label"] == "PERSON") & token_count.eq(1)
    is_generic = canon.isin(GENERIC_STOPLIST)
    is_org_suffix = canon.isin(ORG_SUFFIX_ONLY)

    reason = pd.Series("", index=df.index, dtype="object")
    reason = reason.mask(is_empty, "empty_or_null_entity")
    reason = reason.mask(reason.eq("") & is_numeric, "numeric_only")
    reason = reason.mask(reason.eq("") & is_too_short, "too_short")
    reason = reason.mask(reason.eq("") & is_single_person, "single_token_person_ambiguous")
    reason = reason.mask(reason.eq("") & is_generic, "generic_token_stoplist")
    reason = reason.mask(reason.eq("") & is_org_suffix, "organization_suffix_only")
    return reason


def dominant_label_map(df_kept: pd.DataFrame) -> tuple[pd.Series, set[str]]:
    if df_kept.empty:
        return pd.Series(dtype="object"), set()

    label_counts = (
        df_kept.groupby(["canonical_entity_v1_1", "entity_label"], as_index=False)
        .size()
        .sort_values(["canonical_entity_v1_1", "size"], ascending=[True, False])
    )
    dominant = label_counts.drop_duplicates(subset=["canonical_entity_v1_1"], keep="first")
    dominant_map = dominant.set_index("canonical_entity_v1_1")["entity_label"]
    mult = df_kept.groupby("canonical_entity_v1_1")["entity_label"].nunique()
    mult_set = set(mult[mult > 1].index)
    return dominant_map, mult_set


def reclassify_targets(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    keep_mask = out["entity_quality_flag"] == "keep"

    high = (
        keep_mask
        & out["not_self_mention"].fillna(False).astype(bool)
        & out["tone_std"].fillna("UNKNOWN").isin(TARGET_TONES)
        & out["context_has_attack_term"].fillna(False).astype(bool)
        & out["entity_label"].isin(TARGET_LABELS)
    )

    out["target_confidence_v1_1"] = "low"
    out.loc[high, "target_confidence_v1_1"] = "high"
    out["is_target_v1_1"] = out["target_confidence_v1_1"].eq("high")
    return out


def build_edges_v1_1(df: pd.DataFrame) -> pd.DataFrame:
    target = df[df["is_target_v1_1"]].copy()
    if target.empty:
        cols = [
            "sponsor_name",
            "canonical_entity_v1_1",
            "mention_count",
            "ad_count",
            "platform_count",
            "party_mode",
            "tone_mode",
            "high_confidence_mentions",
            "build_version",
        ]
        return pd.DataFrame(columns=cols)

    grouped = (
        target.groupby(["sponsor_name", "canonical_entity_v1_1"], as_index=False)
        .agg(
            mention_count=("ad_id", "count"),
            ad_count=("ad_id", "nunique"),
            platform_count=("platform", "nunique"),
            party_mode=("party_std", lambda s: s.mode().iloc[0] if not s.mode().empty else "UNKNOWN"),
            tone_mode=("tone_std", lambda s: s.mode().iloc[0] if not s.mode().empty else "UNKNOWN"),
            high_confidence_mentions=("target_confidence_v1_1", lambda s: (s == "high").sum()),
        )
        .sort_values("mention_count", ascending=False)
    )

    filtered = grouped[(grouped["ad_count"] >= 2) & (grouped["mention_count"] >= 2)].copy()
    filtered["build_version"] = BUILD_VERSION
    return filtered


def build_nodes_v1_1(df: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    if edges.empty:
        cols = [
            "canonical_entity_v1_1",
            "mention_count",
            "ad_count",
            "sponsor_count",
            "platform_count",
            "label_mode",
            "high_confidence_mentions",
            "build_version",
        ]
        return pd.DataFrame(columns=cols)

    edge_entities = set(edges["canonical_entity_v1_1"])
    universe = df[df["canonical_entity_v1_1"].isin(edge_entities) & df["is_target_v1_1"]].copy()

    grouped = (
        universe.groupby("canonical_entity_v1_1", as_index=False)
        .agg(
            mention_count=("ad_id", "count"),
            ad_count=("ad_id", "nunique"),
            sponsor_count=("sponsor_name", "nunique"),
            platform_count=("platform", "nunique"),
            label_mode=("entity_label", lambda s: s.mode().iloc[0] if not s.mode().empty else "UNKNOWN"),
            high_confidence_mentions=("target_confidence_v1_1", lambda s: (s == "high").sum()),
        )
        .sort_values("mention_count", ascending=False)
    )
    grouped["build_version"] = BUILD_VERSION
    return grouped


def run_validation(mentions: pd.DataFrame, edges: pd.DataFrame, nodes: pd.DataFrame) -> list[str]:
    warnings: list[str] = []

    required_cols = {
        "canonical_entity_v1_1",
        "entity_quality_flag",
        "drop_reason",
        "is_target_v1_1",
        "target_confidence_v1_1",
    }
    missing = required_cols - set(mentions.columns)
    if missing:
        raise ValueError(f"Mentions output missing required columns: {sorted(missing)}")

    if edges.duplicated(subset=["sponsor_name", "canonical_entity_v1_1"]).any():
        raise ValueError("Duplicate edge keys found in v1.1 edges.")

    kept = mentions[mentions["entity_quality_flag"] == "keep"]
    if kept["canonical_entity_v1_1"].fillna("").eq("").any():
        raise ValueError("Kept rows contain null/blank canonical_entity_v1_1.")

    if not edges.empty:
        if (edges["mention_count"] < 2).any() or (edges["ad_count"] < 2).any():
            raise ValueError("Edge retention threshold violated (mention_count/ad_count >= 2).")

    target_rows = mentions[mentions["is_target_v1_1"]]
    for platform, platform_df in mentions.groupby("platform"):
        if platform_df["is_target_v1_1"].sum() == 0:
            warnings.append(f"warning: zero targets retained for platform={platform}")

    if not nodes.empty:
        node_entities = set(nodes["canonical_entity_v1_1"].astype(str))
        if node_entities & GENERIC_STOPLIST:
            raise ValueError("Generic stoplist token found in final nodes.")
        if any(re.fullmatch(r"\d+", x) for x in node_entities):
            raise ValueError("Numeric-only entity found in final nodes.")
        if any(len(x) <= 2 for x in node_entities):
            raise ValueError("Too-short entity found in final nodes.")

    sponsor_norm = target_rows["sponsor_name"].map(normalize_for_match)
    canon_norm = target_rows["canonical_entity_v1_1"].map(normalize_for_match)
    bad_self = [
        bool(canon) and (canon in sponsor)
        for sponsor, canon in zip(sponsor_norm, canon_norm)
    ]
    if any(bad_self):
        raise ValueError("Found target row where canonical target is substring of normalized sponsor.")

    return warnings


def main() -> int:
    args = parse_args()
    analysis_root = detect_analysis_root()
    mentions_in = resolve_path(args.mentions_in, analysis_root)
    aliases_in = resolve_path(args.aliases_in, analysis_root)
    out_dir = resolve_path(args.out_dir, analysis_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"analysis_root: {analysis_root}")
    print(f"mentions_in: {mentions_in}")
    print(f"aliases_in: {aliases_in}")
    print(f"out_dir: {out_dir}")

    mentions = load_mentions(mentions_in)
    alias = load_alias_map(aliases_in)
    metrics: list[dict[str, object]] = []

    # Baseline metrics from Week 2 table.
    add_metric(metrics, "baseline", "rows_total", len(mentions))
    add_metric(metrics, "baseline", "is_target_rate_v1", float(mentions["is_target"].mean()))
    add_metric(metrics, "baseline", "unique_sponsors_v1", int(mentions["sponsor_name"].nunique()))
    add_metric(metrics, "baseline", "unique_targets_v1", int(mentions["canonical_entity"].nunique()))
    add_metric(metrics, "baseline", "top25_targets_v1", top_targets_string(mentions["canonical_entity"]))

    # Deterministic normalization + alias lock application.
    df = mentions.copy()
    df["entity_text_norm"] = df["entity_text"].map(normalize_for_match)

    alias_for_merge = alias[["entity_text_norm", "entity_label", "canonical_final_norm", "review_status"]]
    df = df.merge(alias_for_merge, on=["entity_text_norm", "entity_label"], how="left", suffixes=("", "_alias"))
    df["review_status"] = df["review_status_alias"].fillna(df.get("review_status", "UNMAPPED")).fillna("UNMAPPED")

    locked = df["review_status"].eq("LOCKED") & df["canonical_final_norm"].fillna("").ne("")
    df["canonical_entity_v1_1"] = df["entity_text_norm"]
    df.loc[locked, "canonical_entity_v1_1"] = df.loc[locked, "canonical_final_norm"]
    df["canonical_entity_v1_1"] = df["canonical_entity_v1_1"].map(normalize_for_match)

    # Conservative entity quality filtering.
    df["drop_reason"] = classify_initial_drop_reason(df)
    df["entity_quality_flag"] = "keep"
    df.loc[df["drop_reason"] != "", "entity_quality_flag"] = "drop"

    # Label-consistency guard among currently kept rows.
    kept = df[df["entity_quality_flag"] == "keep"].copy()
    dominant_map, mult_set = dominant_label_map(kept)
    if mult_set:
        idx = df["canonical_entity_v1_1"].isin(mult_set) & df["entity_quality_flag"].eq("keep")
        dominant_label = df.loc[idx, "canonical_entity_v1_1"].map(dominant_map)
        conflict = idx & df["entity_label"].ne(dominant_label)
        df.loc[conflict, "drop_reason"] = "label_conflict"
        df.loc[conflict, "entity_quality_flag"] = "drop"

    drop_counts = df.loc[df["entity_quality_flag"] == "drop", "drop_reason"].value_counts()
    add_metric(metrics, "post_filter_mentions", "rows_total", len(df))
    add_metric(metrics, "post_filter_mentions", "kept_rows", int((df["entity_quality_flag"] == "keep").sum()))
    add_metric(metrics, "post_filter_mentions", "dropped_rows", int((df["entity_quality_flag"] == "drop").sum()))
    add_metric(metrics, "post_filter_mentions", "keep_rate", float((df["entity_quality_flag"] == "keep").mean()))
    for reason, count in drop_counts.items():
        add_metric(metrics, "post_filter_mentions", f"dropped_reason::{reason}", int(count))

    # Conservative target reclassification.
    df = reclassify_targets(df)
    add_metric(metrics, "post_target_reclass", "rows_total", len(df))
    add_metric(metrics, "post_target_reclass", "target_rows_v1_1", int(df["is_target_v1_1"].sum()))
    add_metric(metrics, "post_target_reclass", "target_rate_v1_1", float(df["is_target_v1_1"].mean()))
    add_metric(
        metrics,
        "post_target_reclass",
        "high_conf_share_among_targets_v1_1",
        float((df.loc[df["is_target_v1_1"], "target_confidence_v1_1"] == "high").mean() if df["is_target_v1_1"].any() else 0.0),
    )

    # Edge/node build.
    edges = build_edges_v1_1(df)
    nodes = build_nodes_v1_1(df, edges)

    add_metric(metrics, "final_edges_nodes", "edge_count_v1_1", len(edges))
    add_metric(metrics, "final_edges_nodes", "node_count_v1_1", len(nodes))
    add_metric(metrics, "final_edges_nodes", "unique_sponsors_v1_1", int(edges["sponsor_name"].nunique() if not edges.empty else 0))
    add_metric(metrics, "final_edges_nodes", "unique_targets_v1_1", int(nodes["canonical_entity_v1_1"].nunique() if not nodes.empty else 0))
    # Use node mention counts, not unique entity-name frequency in the node table.
    top25_v1_1 = "|".join(
        [
            f"{row.canonical_entity_v1_1}:{int(row.mention_count)}"
            for row in nodes.sort_values("mention_count", ascending=False).head(25).itertuples(index=False)
        ]
    )
    add_metric(metrics, "final_edges_nodes", "top25_targets_v1_1", top25_v1_1)
    add_metric(
        metrics,
        "final_edges_nodes",
        "edge_key_duplicates",
        int(edges.duplicated(subset=["sponsor_name", "canonical_entity_v1_1"]).sum()) if not edges.empty else 0,
    )

    warnings = run_validation(df, edges, nodes)
    for warning in warnings:
        add_metric(metrics, "final_edges_nodes", "warning", warning)
        print(warning)

    mentions_out = out_dir / "entity_mentions_week3_cleaned_v1_1.csv.gz"
    edges_out = out_dir / "attack_target_edges_v1_1.csv"
    nodes_out = out_dir / "attack_target_nodes_v1_1.csv"
    metrics_out = out_dir / "cleaning_metrics_v1_1.csv"

    df = df.drop(columns=["review_status_alias", "canonical_final_norm"], errors="ignore")
    df.to_csv(mentions_out, index=False, compression="gzip")
    edges.to_csv(edges_out, index=False)
    nodes.to_csv(nodes_out, index=False)
    pd.DataFrame(metrics).to_csv(metrics_out, index=False)

    print(f"Mentions out: {mentions_out} ({len(df):,} rows)")
    print(f"Edges out: {edges_out} ({len(edges):,} rows)")
    print(f"Nodes out: {nodes_out} ({len(nodes):,} rows)")
    print(f"Metrics out: {metrics_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
