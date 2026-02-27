# Week 3 Target Classification: What Changed and Why

## 1) What qualifies as a target in Week 3 (`v1.1`)

A mention is a target (`is_target_v1_1 = True`) only if **all** of the following are true:

1. `entity_quality_flag == "keep"` (it passes entity cleaning filters).
2. `not_self_mention == True` (target string is not a sponsor self-reference).
3. `tone_std in {"NEGATIVE", "CONTRAST"}`.
4. `context_has_attack_term == True`.
5. `entity_label in {"PERSON", "ORG"}`.

If any condition fails, the mention is `target_confidence_v1_1 = "low"` and `is_target_v1_1 = False`.

## 2) How this differs from Week 2

Week 2 (`v1`) target logic was intentionally permissive:
- `high`: negative/contrast + attack-term + not-self
- `medium`: not-self + (negative/contrast **or** attack-term)
- `is_target = high OR medium`

Week 3 (`v1.1`) is conservative:
- requires the full high-confidence conjunction only.
- excludes `GPE` mentions from target eligibility.
- adds entity-quality filtering before target assignment.
- adds edge retention thresholds: keep only edges with `mention_count >= 2` and `ad_count >= 2`.
- nodes are built only from retained-edge target mentions.

## 3) New cleaning parameters introduced in Week 3

Rows are dropped before targeting if they match any rule:
- `empty_or_null_entity`
- `numeric_only`
- `too_short` (length <= 2)
- `single_token_person_ambiguous`
- `generic_token_stoplist` (`vote`, `senate`, `congress`, `america`, etc.)
- `organization_suffix_only` (`pac`, `inc`, `llc`, `committee`)
- `label_conflict` (entity label disagrees with dominant label for multi-label canonicals)

Observed drop counts:
- `single_token_person_ambiguous`: 14,243
- `generic_token_stoplist`: 8,557
- `label_conflict`: 2,752
- `too_short`: 1,026
- `empty_or_null_entity`: 469
- `organization_suffix_only`: 190
- `numeric_only`: 28

## 4) Concrete Week 2 vs Week 3 differences

### Overall scale shift
- Week 2 target mentions: `77,336` (`60.67%` of mention rows)
- Week 3 target mentions: `10,703` (`8.40%`)
- Week 2 edges: `5,939` -> Week 3 edges: `570`
- Week 2 nodes: `9,744` -> Week 3 nodes: `346`

### Why `congress` disappeared
- Week 2 node mentions for `congress`: `6,351`
- Week 3 node mentions for `congress`: `0`
- Week 3 reason: all `6,351` rows dropped by `generic_token_stoplist`.

### Why `washington` disappeared
- Week 2 node mentions for `washington`: `2,842`
- Week 3 node mentions for `washington`: `0`
- In Week 3, most rows are kept (`2,832`) but target count is `0` because kept `washington` rows are `GPE`, and Week 3 only allows `PERSON`/`ORG` targets.

### Why `donald trump` is lower
- Week 2 node mentions: `2,821`; Week 2 target mentions: `1,836`
- Week 3 node mentions: `225`; Week 3 target mentions: `225`
- Week 3 kept rows for `donald trump`: `2,094`, but only `225` satisfy **all** strict target conditions.
- Also, `727` rows were dropped as `label_conflict`.

### Edge examples (Week 2 -> Week 3)
- `House Majority PAC -> congress`: `455` -> dropped (entity stoplisted).
- `Vote AK Before Party -> alaska`: `373` -> dropped (GPE excluded from target eligibility).
- `Frisch for CO CD-03 -> jeff hurd`: `478` -> `82` (retained, but stricter targeting lowers count).
- `Congressional Leadership Fund -> josh riley`: `381` -> `115` (retained with lower count).
- `NRCC/Molinaro -> mark molinaro`: `300` -> `87` (retained with lower count).

## 5) Consistency check conclusion

The large reductions are consistent with the new conservative settings, not with a pipeline corruption issue:
- target definition is much stricter than Week 2.
- generic/institution terms are intentionally removed.
- GPE mentions are intentionally excluded from target labeling.
- low-support edges are intentionally pruned by thresholding.
