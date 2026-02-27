# Attack-Target Network Progress
**Last updated:** 2026-02-27

## Week 1 Prototype Status

**Status:** Complete (prototype milestone)  
**Notebook reviewed:** `notebooks/week1_attack_target_prototype.ipynb`  
**Outputs directory:** `outputs/week1/`

Week 1 goals from the proposal are complete:
1. Harmonized text table schema created.
2. Text selection and cleaning implemented.
3. NER run on sampled data.
4. Alias-mapping candidate workflow drafted.

## Configuration Snapshot (from notebook run)

- `sample_frac`: `0.02` (2% deterministic sampling)
- `chunk_size`: `100000`
- `max_rows_per_platform`: `35000`
- `min_text_chars`: `20`
- `seed`: `42`
- spaCy model loaded: `en_core_web_sm`

## Week 1 Results

### Harmonized Sample

- Total harmonized rows: **29,830**
- Unique ads: **29,830**
- Date range: **2021-10-03 00:37:52 UTC** to **2024-12-30**
- Missing rate checks:
  - `text_main`: `0.000000`
  - `sponsor_name`: `0.000000`
  - `ad_id`: `0.000000`

| Platform | Rows | Avg text length | Unique sponsors | Share NEGATIVE/CONTRAST |
|---|---:|---:|---:|---:|
| google | 1,599 | 437.499687 | 454 | 0.233271 |
| meta | 9,579 | 318.519052 | 2,390 | 0.132269 |
| tv | 18,652 | 454.857602 | 356 | 0.673547 |

### Entity Extraction (NER)

- Mentions extracted: **127,464**
- Unique entities: **10,367**
- Mention counts by label:
  - `PERSON`: 70,270
  - `ORG`: 30,652
  - `GPE`: 26,542
- Unique entities by label:
  - `PERSON`: 5,390
  - `ORG`: 4,072
  - `GPE`: 1,195

Top extracted entities (by mention count):
1. Congress (`ORG`) - 6,054
2. Washington (`GPE`) - 2,827
3. Medicare (`ORG`) - 2,066
4. Kamala Harris (`PERSON`) - 1,511
5. Alaska (`GPE`) - 1,413
6. America (`GPE`) - 1,191
7. Donald Trump (`PERSON`) - 1,030
8. Josh Riley (`PERSON`) - 1,022
9. Trump (`PERSON`) - 932
10. New York (`GPE`) - 930

### Alias Workflow Artifact

- `outputs/week1/entity_alias_candidates_week1.csv` created with **2,000** high-frequency candidates.
- All 2,000 rows are currently flagged `needs_review=True` (expected for manual canonicalization workflow).

## QA Notes and Risks Identified

- Notebook execution state is clean: all code cells were executed, with no cell errors.
- Early entity ambiguity is visible and expected at prototype stage:
  - multi-label examples include `Trump` (`PERSON` and `ORG`) and `Biden` (`PERSON`/`ORG`/`GPE`).
- This confirms Week 2 must prioritize manual alias locking and target-inference quality controls before graph construction.

## Artifacts Produced

- `outputs/week1/harmonized_sample_week1.parquet`
- `outputs/week1/harmonized_sample_week1.csv.gz`
- `outputs/week1/entity_mentions_week1.parquet`
- `outputs/week1/entity_mentions_week1.csv.gz`
- `outputs/week1/entity_alias_candidates_week1.csv`

## Week 2 Build Status (Current)

**Status:** v1 pipeline outputs generated and organized under `outputs/week2/`.

### Completed Work

1. Built and reviewed alias map starter: `outputs/week1/entity_alias_map_v1.csv`.
2. Completed manual review pass for top 500 alias rows:
   - `LOCKED`: 406
   - `NEEDS_CONTEXT`: 94
   - `DROP`: 25
   - Canonical values changed from suggestion: 110
3. Implemented Week 2 scaffold notebook and script:
   - `notebooks/week2_attack_target_pipeline_scaffold.ipynb`
   - `scripts/week2_build_attack_target_v1.py`
4. Fixed pipeline issues encountered during execution:
   - self-mention check bug (`Series.str.contains(Series)` error) replaced with row-wise comparison.
   - robust project-root path resolution added so script runs from different working directories.
   - Week 2 outputs now default to `outputs/week2/`.

### Week 2 Output Summary (v1)

Artifacts:
- `outputs/week2/attack_target_edges_v1.csv`
- `outputs/week2/attack_target_nodes_v1.csv`
- `outputs/week2/entity_mentions_week2_labeled_v1.csv.gz`

Core counts:
- Labeled mentions: **127,464**
- Inferred target mentions (`is_target=True`): **77,336** (**60.67%**)
- Target confidence distribution:
  - `high`: 16,354
  - `medium`: 60,982
  - `low`: 50,128
- Edge rows: **5,939**
- Unique sponsors in edges: **1,004**
- Unique targets in edges: **3,085**
- Node rows: **9,744**

Platform breakdown (target rate):
- `google`: 2,172 / 5,814 (**37.36%**)
- `meta`: 5,466 / 24,512 (**22.30%**)
- `tv`: 69,698 / 97,138 (**71.75%**)

Alias status coverage on labeled mentions:
- `LOCKED`: 82,198
- `NEEDS_CONTEXT`: 8,780
- `UNMAPPED`: 36,486

Top sponsor->target edges by mention count:
1. `Frisch for CO CD-03 -> jeff hurd` (478)
2. `House Majority PAC -> congress` (455)
3. `House Majority PAC -> medicare` (438)
4. `Vote AK Before Party -> nick begich` (421)
5. `Frisch for CO CD-03 -> adam frisch` (418)

Top nodes by mention count:
1. `congress` (6,351)
2. `kamala harris` (3,082)
3. `washington` (2,842)
4. `donald trump` (2,821)
5. `medicare` (2,070)

### Interpretation Notes / Known Limits

- Current target inference is heuristic and intentionally permissive in v1; precision is not yet measured with manual labels.
- TV has a much higher inferred target rate than digital, likely due to tone mix and context-window behavior; this needs validation before strong substantive interpretation.
- Some high-frequency nodes remain broad institutions/geographies (`congress`, `washington`), which is expected at this stage but should be stress-tested with stricter target rules.

## Updated Next Steps (Week 3)

1. Run manual validation sample (200-400 ads) and report precision for entity extraction, alias mapping, and target inference.
2. Calibrate target rules using validation findings (tighten attack-term lexicon and self-mention exclusion).
3. Expand alias review beyond top 500 (toward top 2,000) to reduce `UNMAPPED` mention share.
4. Generate refined v1.1 outputs (`edges`/`nodes`) and compare against current v1 counts for stability.
5. Start network analytics on validated outputs (centrality, concentration, party/platform splits).

## Week 3 Conservative Build + Interactive App (Current)

**Status:** Complete for conservative `v1.1` data build and Dash-based interactive visualization.

### Week 3 Data Artifacts Produced

- `outputs/week3/entity_mentions_week3_cleaned_v1_1.csv.gz` (127,464 rows; 27 cols)
- `outputs/week3/attack_target_edges_v1_1.csv` (570 rows; 9 cols)
- `outputs/week3/attack_target_nodes_v1_1.csv` (346 rows; 8 cols)
- `outputs/week3/cleaning_metrics_v1_1.csv` (26 rows; 3 cols)

### Week 3 Pipeline Summary

- Conservative mention cleaning applied with explicit `drop_reason`.
- Strict target rule applied (`high` only -> `is_target_v1_1=True`).
- Edge retention threshold enforced (`mention_count >= 2` and `ad_count >= 2`).

Key metrics:
- Week 2 target rate: `60.67%`
- Week 3 target rate: `8.40%`
- Week 2 edges -> Week 3 edges: `5,939 -> 570`
- Week 2 nodes -> Week 3 nodes: `9,744 -> 346`

### Week 3 Interactive App Status

- App: `apps/week3_attack_target_graph_dash.py`
- Implemented:
  - sponsor/target party filters
  - show/hide sponsor/target nodes
  - party vs entity-label coloring
  - topology vs money sizing
  - spend-aware hover metrics
  - neighbor highlight mode
  - accumulate highlight mode

### Week 3 Documentation Added

- `data/docs/WEEK3_DATA_CLEANING_PLAN.md`
- `data/docs/WEEK3_TARGET_CLASSIFICATION_EXPLAINER.md`
- `data/docs/WEEK3_GRAPH_INTERACTIVITY_SPEC.md`
- `data/docs/WEEK3_DASH_APP_GUIDE.md`
- `data/docs/DOCS_INDEX.md`
