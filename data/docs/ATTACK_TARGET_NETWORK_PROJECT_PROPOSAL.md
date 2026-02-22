# Project Proposal: Attack-Target Network in Political Advertising Text

## 1) Project Overview

### Working Title
Attack-Target Network: Mapping Who Attacks Whom Across TV, Meta, and Google Political Ads

### One-Sentence Summary
Build a cross-platform named-entity network from ad text to identify the primary targets of political messaging, how attack focus differs by party and office, and how those patterns vary across media channels.

### Why This Project Matters
Most ad analyses count issue mentions or spend volume. This project adds a strategic layer: it identifies the *interaction structure* of campaigns by modeling sponsor-to-target relationships (who is talking about whom), and links those relationships to tone, issue context, and platform.

## 2) Research Questions and Hypotheses

### Primary Research Question
Who are the most frequent and central attack targets in political ads, and how do those target networks differ by party, office, and platform?

### Secondary Questions
1. Are attack targets concentrated among a small number of national figures, or distributed across local opponents?
2. Do parties differ in target diversity (many targets vs repeated focus on a few)?
3. Does platform context (TV vs Meta vs Google) change who gets targeted and how aggressively?
4. Are certain issues associated with consistent target sets (e.g., immigration-linked targets vs abortion-linked targets)?

### Hypotheses
1. Target concentration hypothesis: a small set of entities will account for a large share of cross-ad mentions.
2. Platform differentiation hypothesis: digital channels will show more rapid and varied target switching than TV.
3. Office specificity hypothesis: local/state races will have denser local-target subgraphs, while federal races connect to a shared national target core.
4. Tone coupling hypothesis: high-negative tone ads will show tighter sponsor-to-target concentration and higher repeat targeting.

## 3) Data Sources

### Primary Files
- `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
- `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`

### Key Text Fields
- Google: `asr_text`, `ocr_text`
- Meta: `ad_creative_body`, `ocr_text`, `ad_creative_link_title`, `ad_creative_link_description`
- TV: `transcript`, `title`

### Key Context Fields
- Sponsor identifiers: `advertiser_name`, `page_name`, `advertiser`
- Party: `party_all` (Google), `party_group` (Meta), `advertiser_party` (TV)
- Office/race context: `office_corrected`, `category`, `race`, `election`
- Tone: `ad_tone`, `ad_tone_constructed`, `tone`
- Issue context: `ISSUE*`, `issue_1`, `issue_2`, `issue_3`

## 4) Conceptual Definitions

### Sponsor Node
The actor paying for/distributing the ad (campaign, party committee, issue group).

### Target Node
A named person, party, administration, or organization mentioned in the ad text as an object of discussion/attack.

### Edge
Directed edge from sponsor node to target node.

### Edge Weight
Number of ad records mentioning that target by that sponsor (optionally weighted by spend/impressions).

### Attack Edge
A sponsor-target edge where text context is negative or attack-oriented (using tone and local sentiment context around mentions).

## 5) Methodology

### Step A: Build Harmonized Text Table
1. Create one normalized table with columns:
- `platform`, `ad_id`, `sponsor_name`, `party_std`, `office_std`, `tone_std`, `issue_context`, `text_main`, `spend_proxy`, `date`
2. Text priority rule:
- Google: `asr_text` then fallback `ocr_text`
- Meta: `ad_creative_body` + key link text, fallback `ocr_text`
- TV: `transcript` fallback `title`
3. Exclude empty/near-empty text rows.

### Step B: Entity Extraction (NER)
1. Run NER on `text_main` (spaCy transformer model or equivalent).
2. Keep entity types: `PERSON`, `ORG`, `GPE` (for location-target analysis extension).
3. Remove low-value generic entities via stoplist (e.g., “America”, “United States” unless analytically needed).

### Step C: Entity Normalization and Canonicalization
1. Normalize casing, punctuation, honorifics, and common variants.
2. Build alias mapping for high-frequency entities (e.g., “President Biden”, “Joe Biden”, “Biden”).
3. Use fuzzy matching plus manual audit for top-N entities by frequency.
4. Maintain a transparent `entity_alias_map.csv` as project artifact.

### Step D: Target Classification
1. Label mention context as likely target vs neutral/self-reference using heuristics:
- Mention near negative verbs/adjectives.
- Mention in ads with negative tone.
- Mention not equal to sponsor identity.
2. Generate confidence flags (`high`, `medium`, `low`) for target inference.

### Step E: Graph Construction
1. Build directed graph `G(sponsor -> target)`.
2. Produce variants:
- Unweighted edge graph
- Mention-count weighted graph
- Spend-weighted graph (when spend comparable)
3. Attach edge attributes:
- platform distribution
- tone mix
- issue tags
- time slices

### Step F: Network Analysis
Compute and compare:
1. Centrality: in-degree, weighted in-degree, PageRank, betweenness
2. Concentration: Herfindahl index of targets by sponsor/party
3. Community detection: modularity-based clusters of sponsor-target blocs
4. Temporal dynamics: monthly target centrality shifts

### Step G: Subgroup Analyses
1. By party
2. By office (`federal`/`state`/`local` as available)
3. By platform
4. By issue families (from `ISSUE*` and `issue_1..3`)

## 6) Validation and Quality Assurance

### Validation Strategy
1. Manual annotation sample (~400 ads) for:
- extracted entities correctness
- canonical entity mapping correctness
- inferred target correctness
2. Measure:
- NER precision/recall on sample
- entity normalization accuracy
- target-inference precision

### Robustness Checks
1. Re-run on high-confidence target edges only.
2. Re-run excluding OCR-only rows.
3. Re-run using stricter mention frequency threshold.
4. Compare results with and without spend weighting.

## 7) Deliverables

### Main Deliverables
1. Final report (`.md` or `.pdf`) with findings and methods.
2. Clean edge list:
- `outputs/attack_target_edges.csv`
3. Node metadata table:
- `outputs/attack_target_nodes.csv`
4. Reproducible analysis notebook/script.

### Core Figures
1. Top 25 target entities by weighted in-degree.
2. Sponsor-to-target network visualization (overall and party-specific).
3. Target concentration by party and platform.
4. Temporal centrality plot for top targets.
5. Issue-conditioned target heatmap.

## 8) Expected Findings (What We Likely See)

1. Heavy concentration on a short list of national political figures.
2. Distinct local clusters in House/state races.
3. Platform-specific emphasis differences (digital more fragmented, TV more repetitive).
4. Strong coupling between negative tone and repeated targeting behavior.

These are expectations, not assumptions; report should explicitly separate observed evidence from prior hypotheses.

## 9) Risks and Mitigation

### Risk 1: NER errors in noisy OCR/ASR text
- Mitigation: confidence filtering + manual review + alias dictionary.

### Risk 2: Ambiguous target inference (mention != attack)
- Mitigation: use tone + local context window + uncertainty flag.

### Risk 3: Cross-platform schema mismatch
- Mitigation: harmonization layer with explicit mapping documentation.

### Risk 4: Compute load on very large files
- Mitigation: chunked processing, sampled prototyping, then full-batch run.

### Risk 5: Over-interpretation of mention networks
- Mitigation: include caveats: mention frequency is a messaging proxy, not voter impact.

## 10) Implementation Plan and Timeline

### Week 1: Data Engineering + Prototype
1. Build harmonized table schema.
2. Implement text selection and cleaning.
3. Run NER on 1-5% sample.
4. Draft alias mapping workflow.

### Week 2: Full Extraction + Validation
1. Full entity extraction.
2. Canonicalization and target inference.
3. Manual validation set and error analysis.
4. Freeze v1 edge list.

### Week 3: Network Analytics + Visualization
1. Compute centrality/concentration/community outputs.
2. Run subgroup and temporal analyses.
3. Generate figure set and interpretation notes.

### Week 4: Write-up + Robustness
1. Complete robustness checks.
2. Finalize methods appendix and caveats.
3. Ship final report + reproducible scripts.

## 11) Success Criteria

1. Reproducible pipeline from raw text fields to final network tables.
2. At least 3 non-trivial, defensible findings about target structure.
3. Clear uncertainty handling (confidence flags + sensitivity tests).
4. Outputs reusable for follow-up projects (tone, issues, persuasion strategy).

## 12) Optional Stretch Goals

1. Add stance detection around mentions (support/attack/neutral).
2. Build race-level mini-networks and compare competitiveness buckets.
3. Integrate geospatial targeting fields for “target mention vs target geography” mismatch.
4. Build interactive network dashboard (Plotly/pyvis).

## 13) Resource Requirements

1. Python stack: `pandas`, `pyarrow`, `spacy`, `networkx`, `matplotlib/seaborn`, optional `sentence-transformers`.
2. Disk: sufficient temp space for decompression/chunk processing.
3. Compute: local feasible with chunking; GPU optional but not required.

## 14) Decision Rules (Locked for v1)

### 14.1 Canonical Party Mapping Rule

Use a standardized field `party_std` with categories:
- `DEM`
- `REP`
- `IND`
- `NONPARTISAN`
- `OTHER`
- `UNKNOWN`

Platform-specific source priority:
1. Google: use `party_all` as primary party source.
2. Meta: use `party_group` as primary source; fallback to `party_cdptyonly` when available.
3. TV: use `advertiser_party` as primary source.

Implementation requirements:
1. Keep both raw and standardized fields: `party_raw`, `party_std`.
2. Add provenance field `party_source` (e.g., `party_all`, `party_group`, `advertiser_party`).
3. Add quality field `party_confidence` (`high`, `medium`, `low`) based on mapping certainty.

### 14.2 Primary Tone Variable Preference by Platform

Use standardized field `tone_std` with categories:
- `POSITIVE`
- `NEGATIVE`
- `CONTRAST`
- `MIXED`
- `UNKNOWN`

Platform-specific tone fallback chain:
1. Google: `ad_tone` -> `ad_tone_constructed` -> `UNKNOWN`
2. Meta: `ad_tone` -> `ad_tone_constructed` -> `UNKNOWN`
3. TV: `tone` -> `UNKNOWN`

Implementation requirements:
1. Preserve `tone_raw` and `tone_std`.
2. Preserve provenance field `tone_source`.
3. Report coverage diagnostics by platform for each tone source.

### 14.3 Threshold for Defining Attack Edges

Define row-level `attack_score` as:
1. `+1` if target entity is not the sponsor identity.
2. `+1` if `tone_std` is `NEGATIVE` or `CONTRAST`.
3. `+1` if attack lexicon appears in a local context window around the entity mention.

Row-level attack classification:
- `is_attack = 1` if `attack_score >= 2`
- `is_attack = 0` otherwise

Edge retention threshold for main graph:
1. Keep sponsor-target edges with at least `2` distinct ads satisfying `is_attack = 1`.
2. For sensitivity analysis, also report:
- strict graph: `>=3` ads
- permissive graph: `>=1` ad

### 14.4 Target Entity Scope (Person vs Organization)

Include both target types in extraction:
- `PERSON`
- `ORG`

Reporting policy:
1. Main results and headline figures use `PERSON` targets only.
2. Secondary appendix includes combined `PERSON + ORG` network.
3. Every node/edge must include `target_type` for explicit filtering.

---
Prepared for: Attack-Target NLP Analysis Project
Status: Proposal Draft v1.1




This project proposal is **exceptionally strong** and aligns perfectly with the research trajectories established in the provided sources. It moves beyond descriptive statistics (e.g., volume of ads) to analyze the **strategic interaction structure** of modern campaigning.

Below is an evaluation of the proposal based on its feasibility, meaningfulness, and potential for impact using the available 2024 datasets.

### 1. Feasibility (Score: 10/10)
The data required to execute this project is already present and well-structured in your primary files:
*   **Target Detection:** The 2024 digital datasets (`google2024_set1` and `meta2024_set1`) contain fields specifically designed for this: `detected_entities_federal` (for text mentions) and `aws_face_federal` (for visual appearances in images or video frames). 
*   **Sponsor Identification:** The data includes `pd_id` (page-disclaimer identifiers) and `sponsor_type` (candidate, party, or group), which are essential for defining your "Sponsor Nodes".
*   **Attack Classification:** The `ad_tone_constructed` variable in the 2024 data classifies ads into "attack," "contrast," and "promote" based on sentiment and entity mention patterns. This directly facilitates the creation of "Attack Edges."

### 2. Academic Meaningfulness (Score: 9.5/10)
This project addresses several core theories in political science discussed in the sources:
*   **The "Proxy" Attack Strategy:** Research consistently shows that interest groups and parties act as **"attack dogs"** to shield candidates from the **backlash effect** associated with negativity. Your network analysis would provide empirical proof of how these groups are structurally linked to specific targets on behalf of their favored candidates.
*   **Nationalization of Politics:** The sources note a trend where local House races increasingly resemble Senate races, focusing more on national party control than local issues. Your **Hypothesis 3** (Office Specificity) would provide a definitive measure of whether "attack targets" are being nationalized (e.g., everyone attacking Harris/Trump) or remaining localized to opponents.
*   **Platform Differentiation:** The sources highlight that Meta is primarily used for **fundraising and mobilization**, while Google (YouTube) and TV are used for **persuasion**. Mapping the attack-target network across these platforms will reveal if "attack messaging" is a tool for raising money (Meta) or shifting votes (Google/TV).

### 3. Interestingness & Potential Insights (Score: 10/10)
*   **Target Centrality:** It would be highly interesting to see if specific national figures (like Nancy Pelosi in 2010) remain "central nodes" in the 2024 network or if the target set has become more fragmented.
*   **The "Democratic Ad Advantage":** Since Democrats outspent Republicans significantly in 2024 digital ads, the network would reveal if this extra cash was used for **targeted surgical strikes** on many small entities or a **massive concentrated bombardment** on a single target.
*   **Issue-Target Coupling:** Linking targets to issues (e.g., linking specific figures to "immigration" vs. "abortion") would add a layer of "Issue Ownership Theory" to your network analysis.

### 4. Strengths of the Proposal
*   **Cross-Medium Focus:** Comparing the "Interaction Structure" of TV vs. Digital is critical, as sources suggest digital is often a "nicer" environment with fewer pure attacks.
*   **Methodological Rigor:** The focus on "directed edges" and "edge weight" (weighted by spend) is the correct approach to account for **ad distribution**, as ad IDs alone are not meaningful measures of volume.

### 5. Recommended Adjustments based on Sources
*   **Sponsor Node Grouping:** You should consider the finding that many Super PACs and Carey PACs are **parallel party-like committees** (e.g., Senate Leadership Fund). In your analysis, it may be more meaningful to "collapse" or "cluster" these nodes by party affiliation to see the true "Party vs. Party" attack structure.
*   **Visual vs. Textual:** The sources warn that relying solely on text/audio might under-report mentions. Ensure your "Attack Edge" definition heavily weights the `aws_face_federal` field, as candidates (particularly in 2024) were often **pictured in negative contexts** without being named in the text.
*   **Demographic Nuance:** If you pursue your "Stretch Goals," integrating Meta’s **demographic impression shares** would be high-impact. It could show if certain "Attack Targets" are being delivered specifically to certain age or gender cohorts (e.g., attacking a candidate on abortion primarily in ads seen by women).

**Overall Verdict:** This is a **high-caliber project** that utilizes the best features of the 2024 datasets. It is structurally sound and addresses a significant gap in current ad research by modeling the **interactional strategy** of campaigns.