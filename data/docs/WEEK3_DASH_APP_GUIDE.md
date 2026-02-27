# Week 3 Dash App Guide

## Purpose
This app provides an interactive view of the Week 3 conservative attack-target network with:
- party filters,
- node visibility controls,
- multiple color/size modes,
- spend-aware hover context,
- click-driven neighborhood highlighting.

App entrypoint:
- `analysis/apps/week3_attack_target_graph_dash.py`

## Run
From `analysis/`:

```bash
poetry run python apps/week3_attack_target_graph_dash.py
```

Open:
- `http://127.0.0.1:8050`

## Data Inputs Used by the App
- `outputs/week3/attack_target_edges_v1_1.csv`
- `outputs/week3/attack_target_nodes_v1_1.csv`
- `outputs/week3/entity_mentions_week3_cleaned_v1_1.csv.gz`
- `outputs/week1/harmonized_sample_week1.csv.gz` (for `spend_proxy`)

## Core Controls

### Filters
- **Sponsor Party Filter**: keep edges from selected sponsor parties.
- **Target Party Filter (Inferred)**: keep edges to selected inferred target-party groups.
- **Show Node Types**: show/hide sponsors and targets.
- **Min Edge Mentions**: minimum edge `mention_count`.
- **Top N Edges**: cap rendered edges after filtering/sorting.

### Visual Modes
- **Color Mode**
  - `Party Colors`
  - `Entity Label Colors`
- **Size Mode**
  - `Topology`: sponsors by out-degree, targets by in-degree
  - `Money`: sponsors by total attack spend, targets by total received attack spend

### Interaction Mode
- **Neighbor Highlight** (default):
  - one selected seed node at a time.
- **Accumulate Highlight**:
  - each click adds that node’s neighborhood to highlighted subnet.
  - clicking an already-seeded node removes it.
- **Clear Selection**:
  - clears all selected seed nodes.

## Visual Semantics

### Role cue
- Sponsors are **squares**.
- Targets are **circles**.

### Party colors
- Sponsors:
  - `REP` red, `DEM` blue, `IND` green, `OTHER/UNKNOWN` gray.
- Targets:
  - target colors are intentionally flipped between `REP`/`DEM` relative to sponsors to support “opposed-side” reading in this app configuration.

## Hover Information

### Sponsor hover
- sponsor name
- sponsor party
- outgoing edge count
- total attack spend (`sponsor_attack_spend`)

### Target hover
- target name
- label type
- inferred target party
- incoming edge count
- total received attack spend (`target_received_spend`)

## Spend Definitions
- Spend metric uses `spend_proxy` from Week 1 harmonized ad table.
- Spend joins on `(platform, ad_id)`.
- Spend aggregation is deduplicated at ad level to avoid double counting repeated mention rows.

## Notes
- This app is live-interactive; static HTML exports from other scripts do not include Dash callback behavior.
- If you update underlying Week 3 CSVs, restart the Dash app to reload runtime data.
