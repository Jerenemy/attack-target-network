# Attack-Target Classification Explainer (Current Approach)

## Why this matters
For this project, we are trying to label when a sponsor is attacking a person or organization in ad text.  
If this rule is too loose, the graph gets noisy. If it is too strict, we miss real attacks.

## Why "opposite party mention" is not enough by itself
A simple idea is:
- if a Republican sponsor mentions a Democrat (or vice versa), treat that as an attack.

This helps, but it is not reliable on its own.

Why:
1. Not every cross-party mention is an attack.
   - Example: neutral attribution like "Kamala says..." or "Trump supports...".
2. Some mentions are contrastive but not direct attacks.
3. Same-party attacks (especially primaries) can happen and would be missed.
4. Some mentions are generic narrative context, not true target claims.

So opposite-party status is useful as a feature, but not a definitive label by itself.

## What we currently use (Week 3 `v1.1`)
A mention is counted as a target attack (`is_target_v1_1=True`) only if all of these are true:

1. Mention passed quality filtering (`entity_quality_flag = keep`).
2. Not a sponsor self-mention (`not_self_mention = True`).
3. Ad tone is `NEGATIVE` or `CONTRAST`.
4. Mention context contains an attack term (`context_has_attack_term = True`).
5. Entity label is `PERSON` or `ORG` (not `GPE`).

If any fail, that mention is not counted as a target attack in Week 3.

## Attack-term list currently used
The current lexicon (from Week 2 pipeline, reused in Week 3 fields):

- `failed`
- `failure`
- `dangerous`
- `corrupt`
- `lies`
- `lying`
- `radical`
- `extreme`
- `crime`
- `criminal`
- `inflation`
- `border`
- `illegal`
- `tax`

How applied:
- We check the mention `context_window`.
- If any of the above terms appears, `context_has_attack_term=True`.

## Mock example (how counting works)
Suppose this ad:

- Sponsor: `Committee X`
- Tone: `NEGATIVE`
- Transcript:
  - "Kamala Harris failed at the border."
  - "Harris supports dangerous policies."

Processing result:
1. NER finds two mentions of `kamala harris`.
2. Both mentions have attack terms (`failed`, `dangerous`) in context.
3. Both pass the Week 3 rule.

So for edge `Committee X -> kamala harris`:
- `mention_count` increases by **2** (two qualifying mentions)
- `ad_count` increases by **1** (one distinct ad)

If another ad contributes one qualifying mention:
- `mention_count = 3`
- `ad_count = 2`

## Important clarification: mention count vs unique ads
- `mention_count` = number of qualifying mention rows.
- `ad_count` = number of unique ads (`ad_id`) contributing to that edge.

So yes, one ad can contribute multiple mentions.

## Spend and duplicate-count guardrails
For spend metrics in the Dash app, we guard against duplicate inflation:
- Sponsor spend dedupes by `sponsor + platform + ad_id`.
- Target spend dedupes by `target + platform + ad_id`.
- Edge spend dedupes by `sponsor + target + platform + ad_id`.

This means repeated mentions in the same ad do not multiply spend totals.

## What spend represents
Spend here is based on `spend_proxy` from harmonized ad data, which is an airing/delivery spend proxy (or midpoint), not creative production cost.

## Files implementing this logic
- Week 2 attack-term/context setup:
  - `analysis/scripts/week2_build_attack_target_v1.py`
- Week 3 strict target classification:
  - `analysis/scripts/week3_clean_attack_target_v1_1.py`
- Dash app spend/hover aggregation:
  - `analysis/apps/week3_attack_target_graph_dash.py`
