# Week 3 Graph Interactivity Spec

## Objective
Define and implement a richer interactive graph experience for Week 3 so users can:
- filter what is visible,
- compare partisan patterns quickly (red Republican, blue Democrat),
- inspect spend context in attack relationships,
- and explore local neighborhoods by clicking sponsors or targets.

## Current vs New Functionality

| Feature | Status | Where |
|---|---|---|
| Basic pan/zoom/hover interactive graph | Already implemented | `scripts/week3_build_attack_target_graph_interactive_v1_1.py` |
| CLI edge thresholds (`--min-edge-mentions`, `--top-n-edges`) | Already implemented | `scripts/week3_build_attack_target_graph_interactive_v1_1.py` |
| Largest-component filtering via CLI | Already implemented | `scripts/week3_build_attack_target_graph_interactive_v1_1.py` |
| Hover basics (mentions/ads/platforms) | Already implemented | `scripts/week3_build_attack_target_graph_interactive_v1_1.py` |
| In-UI party filters for sponsors and targets | Implemented (new) | `apps/week3_attack_target_graph_dash.py` |
| In-UI show/hide sponsors and targets | Implemented (new) | `apps/week3_attack_target_graph_dash.py` |
| Party color mode (sponsors standard, targets configured with flipped DEM/REP mapping) | Implemented (new) | `apps/week3_attack_target_graph_dash.py` |
| Sponsor size by outgoing edges | Implemented (new) | `apps/week3_attack_target_graph_dash.py` (`size_mode=topology`) |
| Sponsor attack-spend in hover | Implemented (new) | `apps/week3_attack_target_graph_dash.py` |
| Toggle size by money for sponsors/targets | Implemented (new) | `apps/week3_attack_target_graph_dash.py` (`size_mode=money`) |
| Click sponsor -> highlight connected targets, dim others | Implemented (new) | `apps/week3_attack_target_graph_dash.py` (`interaction_mode=highlight` / `accumulate`) |
| Click target -> highlight connected sponsors, dim others | Implemented (new) | `apps/week3_attack_target_graph_dash.py` (`interaction_mode=highlight` / `accumulate`) |
| Multi-click accumulating highlight subnetworks | Implemented (new) | `apps/week3_attack_target_graph_dash.py` (`interaction_mode=accumulate`) |

## Inputs
- `outputs/week3/attack_target_edges_v1_1.csv`
- `outputs/week3/attack_target_nodes_v1_1.csv`
- `outputs/week3/entity_mentions_week3_cleaned_v1_1.csv.gz`
- `outputs/week1/harmonized_sample_week1.csv.gz` (for `spend_proxy`)

## Derived Runtime Fields
- `node_type`: `sponsor` or `target`
- `sponsor_party`: modal party by sponsor from mention records (`party_std`)
- `target_party_inferred`: incoming-edge weighted majority party by `mention_count`; ties => `UNKNOWN`
- `sponsor_out_degree`: number of outgoing sponsor edges in current filtered view
- `sponsor_attack_spend`: sum of `spend_proxy` across unique sponsor attack ads (`sponsor_name + platform + ad_id`)
- `target_received_spend`: sum of `spend_proxy` across unique target attack ads (`canonical_entity_v1_1 + platform + ad_id`)
- `edge_attack_spend`: spend allocated to each sponsor-target edge (`sponsor + target + platform + ad_id`, deduped)

## Exact Interaction Behavior

### 1) Party filters
- Sponsor-party filter keeps only edges where sponsor party is selected.
- Target-party filter keeps only edges where inferred target party is selected.

### 2) Hide/show node classes
- `sponsor` and `target` visibility toggles control whether those node classes are rendered.
- Hidden node classes suppress incident edges from view.

### 3) Color modes
- `party` mode:
  - sponsors: `REP = #d62728` (red), `DEM = #1f77b4` (blue)
  - targets: configured with flipped `REP/DEM` mapping for opposed-side interpretation
  - `IND = #2ca02c`
  - `OTHER/UNKNOWN = gray`
- `entity_label` mode:
  - targets use PERSON/ORG/GPE palette
  - sponsors use sponsor gray

### 4) Size modes
- `topology` mode:
  - sponsor size scales by outgoing edge count in current filtered graph
  - target size scales by incoming edge count in current filtered graph
- `money` mode:
  - sponsor size scales by `sponsor_attack_spend`
  - target size scales by `target_received_spend`

### 5) Click highlight modes
- `highlight` mode:
  - single selected seed node at a time
  - clicking a sponsor highlights sponsor + outgoing targets + those edges
  - clicking a target highlights target + incoming sponsors + those edges
  - clicking the same node again clears selection
- `accumulate` mode:
  - each click adds the node's neighborhood to the active highlighted subnetwork
  - clicking an already-selected node removes it from active seeds
- Both modes:
  - non-neighbor nodes and edges are dimmed
  - `Clear Selection` resets all active seeds

## Spend Semantics
- Spend uses `spend_proxy` from Week 1 harmonized ads.
- Null spend is treated as `0.0`.
- Spend totals are deduplicated at ad level before aggregation to avoid repeated counting from multiple mention rows.

## Acceptance Checks
1. Sponsor REP/DEM color mapping is correct in party mode, and target color mapping follows configured flipped logic.
2. Sponsor hover includes total attack spend.
3. Target hover includes received attack spend.
4. Topology size mode visibly enlarges high out-degree sponsors.
5. Money size mode changes node sizes relative to spend.
6. Party filters and node-type toggles change visible node/edge counts.
7. Highlight mode shows only selected neighborhood at high opacity.
8. Accumulate mode adds/removes neighborhoods correctly across repeated clicks.

## Run Instructions
From `analysis/`:

```bash
poetry run python apps/week3_attack_target_graph_dash.py
```

Open `http://127.0.0.1:8050` in browser.
