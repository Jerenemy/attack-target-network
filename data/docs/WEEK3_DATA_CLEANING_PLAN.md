# Week 3 Plan: Conservative Data Cleaning for Attack-Target Graph v1.1

## Objective
Improve graph quality without manual verification by applying deterministic, conservative cleaning to Week 2 mention/edge/node artifacts, then producing side-by-side `v1.1` outputs (keeping `v1` unchanged).

This plan prioritizes precision over coverage:
- Remove low-information/noisy entities.
- Tighten target inference eligibility.
- Prevent obvious false sponsor->target edges.
- Preserve full auditability with explicit reason codes.

Primary inputs:
- `analysis/outputs/week2/entity_mentions_week2_labeled_v1.csv.gz`
- `analysis/outputs/week1/entity_alias_map_v1.csv`

Primary outputs:
- `analysis/outputs/week3/entity_mentions_week3_cleaned_v1_1.csv.gz`
- `analysis/outputs/week3/attack_target_edges_v1_1.csv`
- `analysis/outputs/week3/attack_target_nodes_v1_1.csv`
- `analysis/outputs/week3/cleaning_metrics_v1_1.csv`

## Important API / Interface / Type Changes
1. New script: `analysis/scripts/week3_clean_attack_target_v1_1.py`
2. CLI interface (fixed defaults, no ambiguity):
   - `--mentions-in` default `outputs/week2/entity_mentions_week2_labeled_v1.csv.gz`
   - `--aliases-in` default `outputs/week1/entity_alias_map_v1.csv`
   - `--out-dir` default `outputs/week3`
3. Mention schema additions:
   - `canonical_entity_v1_1` (string)
   - `entity_quality_flag` (`keep`, `drop`)
   - `drop_reason` (enum string; empty if kept)
   - `is_target_v1_1` (bool)
   - `target_confidence_v1_1` (`high`, `low`)
4. Edge schema changes for v1.1:
   - built only from `is_target_v1_1 == True`
   - adds `build_version = "v1.1_conservative"`
5. Node schema changes for v1.1:
   - recomputed from cleaned mentions only
   - adds `build_version = "v1.1_conservative"`

## Cleaning Rules (Verbatim)
1. Baseline profiling snapshot
- Compute and store baseline counts from Week 2 (`rows`, `is_target` share, unique sponsors/targets, top nodes).
- Write to `cleaning_metrics_v1_1.csv` as `stage=baseline`.

2. Deterministic normalization pass
- Recompute `entity_text_norm` and `canonical_entity_v1_1` with strict lowercase + punctuation strip + whitespace collapse.
- If alias map has `review_status == LOCKED`, force canonical to locked `canonical_final`.
- If alias map is `NEEDS_CONTEXT` or unmapped, keep normalized entity text as provisional canonical.

3. Entity quality filtering (conservative)
Mark `entity_quality_flag=drop` with one explicit `drop_reason` when any rule matches:
- `empty_or_null_entity`: null/blank canonical.
- `numeric_only`: canonical matches `^\d+$`.
- `too_short`: canonical length <= 2.
- `single_token_person_ambiguous`: `entity_label == PERSON` and token count == 1.
- `generic_token_stoplist`: canonical in fixed stoplist:
  - `vote`, `votes`, `voting`, `senate`, `congress`, `america`, `country`, `state`, `states`, `people`, `children`, `taxpayer`, `taxpayers`
- `organization_suffix_only`: canonical in `{pac, inc, llc, committee}`.
All non-dropped rows are `entity_quality_flag=keep`.

4. Label-consistency guard
- Compute dominant label per `canonical_entity_v1_1` from kept rows.
- If a row’s label differs from dominant label and canonical has multi-label history, set `drop_reason=label_conflict` and drop.

5. Conservative target reclassification
For kept rows only:
- `target_confidence_v1_1 = high` iff all true:
  - `not_self_mention == True`
  - `tone_std in {NEGATIVE, CONTRAST}`
  - `context_has_attack_term == True`
  - `entity_label in {PERSON, ORG}`
- Else `target_confidence_v1_1 = low`
- `is_target_v1_1 = (target_confidence_v1_1 == "high")`

6. Edge/node rebuild rules
- Edges from rows with `is_target_v1_1 == True`.
- Group key: `(sponsor_name, canonical_entity_v1_1)`.
- Retain edges only when:
  - `ad_count >= 2`
  - `mention_count >= 2`
- Nodes from retained-edge mention universe only.

7. Metrics + QA artifact generation
Append stages to `cleaning_metrics_v1_1.csv`:
- `post_filter_mentions`
- `post_target_reclass`
- `final_edges_nodes`
Include: row counts, dropped rows by reason, target share, edge count, node count, unique sponsors, unique targets.

## Acceptance Checks
1. Schema tests
- Required new columns exist in mention/edge/node outputs.
- No duplicate edge keys `(sponsor_name, canonical_entity_v1_1)`.

2. Integrity tests
- `canonical_entity_v1_1` has no nulls in kept rows.
- All final edges satisfy `mention_count >= 2` and `ad_count >= 2`.
- All edge source rows have `is_target_v1_1 == True`.

3. Rule enforcement tests
- No final node entity equals a generic stoplist token.
- No `numeric_only` or `too_short` entity appears in final nodes.
- No final edge where canonical target is exact substring match of normalized sponsor name.

4. Regression comparison scenarios (v1 vs v1.1)
- Edge count decreases (expected with conservative filtering).
- Share of high-confidence targets among retained targets is 100% by construction.
- Top-25 targets should shift away from generic nouns toward named actors; record before/after table in metrics artifact.

5. Failure-mode scenarios
- If alias file missing required columns -> hard fail with explicit error.
- If filtering removes all targets on a platform -> emit warning in metrics and still write outputs.

## Caveats
- Manual verification is intentionally deferred for Week 3.
- Conservative precision is prioritized over recall.
- Existing Week 2 artifacts remain immutable.
- Output versioning is side-by-side (`v1` + `v1.1`).
