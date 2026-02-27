#!/usr/bin/env python3
"""Build an interactive Week 3 attack-target graph HTML in one command.

Default usage:
    poetry run python scripts/week3_build_attack_target_graph_interactive_v1_1.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.graph_objects as go


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Week 3 v1.1 interactive attack-target graph.")
    parser.add_argument(
        "--edges",
        default="outputs/week3/attack_target_edges_v1_1.csv",
        help="Path to Week 3 edge CSV.",
    )
    parser.add_argument(
        "--nodes",
        default="outputs/week3/attack_target_nodes_v1_1.csv",
        help="Path to Week 3 node CSV.",
    )
    parser.add_argument(
        "--out-html",
        default="outputs/week3/attack_target_graph_interactive_v1_1.html",
        help="Output HTML path.",
    )
    parser.add_argument(
        "--min-edge-mentions",
        type=int,
        default=2,
        help="Minimum mention_count edge threshold.",
    )
    parser.add_argument(
        "--top-n-edges",
        type=int,
        default=700,
        help="Maximum number of edges to plot after filtering.",
    )
    parser.add_argument(
        "--keep-largest-component",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Keep only the largest weakly-connected component (use --no-keep-largest-component to disable).",
    )
    parser.add_argument(
        "--layout-k",
        type=float,
        default=0.42,
        help="Spring layout k parameter.",
    )
    parser.add_argument(
        "--layout-seed",
        type=int,
        default=42,
        help="Spring layout seed.",
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
        if (candidate / "data").exists() and (candidate / "outputs").exists():
            return candidate
    return cwd


def resolve_path(path_str: str, analysis_root: Path) -> Path:
    path = Path(path_str).expanduser()
    return path if path.is_absolute() else (analysis_root / path).resolve()


def scale_size(value: float, min_value: float, max_value: float, lo: float = 8, hi: float = 42) -> float:
    if max_value == min_value:
        return (lo + hi) / 2
    return lo + (value - min_value) * (hi - lo) / (max_value - min_value)


def main() -> int:
    args = parse_args()
    analysis_root = detect_analysis_root()

    edge_path = resolve_path(args.edges, analysis_root)
    node_path = resolve_path(args.nodes, analysis_root)
    out_html = resolve_path(args.out_html, analysis_root)
    out_html.parent.mkdir(parents=True, exist_ok=True)

    if not edge_path.exists():
        raise FileNotFoundError(f"Edges file not found: {edge_path}")
    if not node_path.exists():
        raise FileNotFoundError(f"Nodes file not found: {node_path}")

    edges = pd.read_csv(edge_path)
    nodes = pd.read_csv(node_path)

    edges_f = edges.copy()
    edges_f = edges_f[edges_f["mention_count"] >= args.min_edge_mentions]
    edges_f = edges_f.sort_values("mention_count", ascending=False)
    if args.top_n_edges is not None:
        edges_f = edges_f.head(args.top_n_edges)

    graph = nx.DiGraph()
    for row in edges_f.itertuples(index=False):
        graph.add_edge(
            row.sponsor_name,
            row.canonical_entity_v1_1,
            mention_count=int(row.mention_count),
            ad_count=int(row.ad_count),
            platform_count=int(getattr(row, "platform_count", 0)),
            party_mode=getattr(row, "party_mode", "UNKNOWN"),
            tone_mode=getattr(row, "tone_mode", "UNKNOWN"),
        )

    node_lookup = (
        nodes.groupby("canonical_entity_v1_1", as_index=False)
        .agg(
            mention_count=("mention_count", "max"),
            ad_count=("ad_count", "max"),
            sponsor_count=("sponsor_count", "max"),
            platform_count=("platform_count", "max"),
            label_mode=("label_mode", lambda s: s.mode().iloc[0] if not s.mode().empty else "SPONSOR_OR_UNMAPPED"),
        )
        .set_index("canonical_entity_v1_1")
        .to_dict("index")
    )

    for node in list(graph.nodes()):
        meta = node_lookup.get(node, {})
        graph.nodes[node]["mention_count"] = int(meta.get("mention_count", 1))
        graph.nodes[node]["ad_count"] = int(meta.get("ad_count", 1))
        graph.nodes[node]["sponsor_count"] = int(meta.get("sponsor_count", 1))
        graph.nodes[node]["platform_count"] = int(meta.get("platform_count", 1))
        graph.nodes[node]["label_mode"] = meta.get("label_mode", "SPONSOR_OR_UNMAPPED")

    if args.keep_largest_component and graph.number_of_nodes() > 0:
        components = list(nx.weakly_connected_components(graph))
        largest = max(components, key=len)
        graph = graph.subgraph(largest).copy()

    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty after filtering. Lower --min-edge-mentions or increase --top-n-edges.")

    pos = nx.spring_layout(graph, k=args.layout_k, seed=args.layout_seed)

    label_colors = {
        "PERSON": "#1f77b4",
        "ORG": "#d62728",
        "GPE": "#2ca02c",
        "SPONSOR_OR_UNMAPPED": "#7f7f7f",
    }

    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for u, v in graph.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        hoverinfo="none",
        showlegend=False,
        line=dict(width=0.7, color="rgba(120,120,120,0.35)"),
    )

    node_mentions = pd.Series({n: graph.nodes[n].get("mention_count", 1) for n in graph.nodes()})
    min_m = float(node_mentions.min())
    max_m = float(node_mentions.max())

    node_x: list[float] = []
    node_y: list[float] = []
    node_size: list[float] = []
    node_color: list[str] = []
    node_text: list[str] = []

    for n in graph.nodes():
        x, y = pos[n]
        meta = graph.nodes[n]
        label = meta.get("label_mode", "SPONSOR_OR_UNMAPPED")
        node_x.append(x)
        node_y.append(y)
        node_size.append(scale_size(float(meta.get("mention_count", 1)), min_m, max_m))
        node_color.append(label_colors.get(label, "#7f7f7f"))
        node_text.append(
            f"node={n}<br>"
            f"label={label}<br>"
            f"mentions={meta.get('mention_count', 0):,}<br>"
            f"ads={meta.get('ad_count', 0):,}<br>"
            f"sponsors={meta.get('sponsor_count', 0):,}<br>"
            f"platforms={meta.get('platform_count', 0):,}"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        showlegend=False,
        marker=dict(
            size=node_size,
            color=node_color,
            opacity=0.95,
            line=dict(width=0.8, color="rgba(255,255,255,0.85)"),
        ),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=(
            f"Week 3 Attack-Target Graph v1.1: "
            f"{graph.number_of_nodes():,} nodes, {graph.number_of_edges():,} edges"
        ),
        template="plotly_white",
        hovermode="closest",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )

    fig.write_html(str(out_html), include_plotlyjs="cdn")
    print(f"wrote: {out_html}")
    print(f"nodes plotted: {graph.number_of_nodes():,}")
    print(f"edges plotted: {graph.number_of_edges():,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
