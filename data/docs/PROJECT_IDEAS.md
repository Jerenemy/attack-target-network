# Project Ideas for `analysis/data`

Scoring scale: 1-10 (10 is best).
- Feasibility: how easy it is to execute with current files
- Impact: substantive or policy relevance
- Interestingness: how compelling the story/question is
- Novelty: how non-obvious the result is likely to be
- Data Readiness: how directly available required fields are
- Compute Efficiency: 10 means low compute burden
- Overall: holistic project quality score

## Ranked Idea Table

| Rank | Project Idea | Feasibility | Impact | Interestingness | Novelty | Data Readiness | Compute Efficiency | Overall |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Cross-platform issue agenda alignment (TV vs Meta vs Google) | 8 | 9 | 9 | 8 | 8 | 6 | 8.4 |
| 2 | Geographic targeting congruence (where ads run vs where they mention) | 8 | 8 | 8 | 8 | 8 | 7 | 8.0 |
| 3 | Candidate vs group strategy gap (issue mix, tone, spend patterns) | 9 | 7 | 8 | 6 | 9 | 9 | 7.8 |
| 4 | 2024 to 2026 issue shift tracking | 9 | 7 | 7 | 6 | 9 | 8 | 7.7 |
| 5 | Goal model behavior in digital ads (Persuade/Donate/GOTV probabilities) | 7 | 8 | 8 | 8 | 7 | 6 | 7.7 |
| 6 | Language and outreach segmentation (English vs Spanish-related issue activity) | 8 | 7 | 7 | 7 | 8 | 8 | 7.6 |
| 7 | Tone polarization by party and office type | 9 | 7 | 7 | 5 | 9 | 9 | 7.5 |
| 8 | Spend efficiency by issue and medium (cost per reach/viewing proxy) | 7 | 8 | 8 | 7 | 7 | 5 | 7.4 |
| 9 | Market-level saturation and overlap dynamics in TV | 6 | 8 | 8 | 7 | 6 | 5 | 7.0 |
| 10 | Human-coded vs AI-coded consistency audit (legacy TV vs newer TV schema) | 5 | 9 | 9 | 9 | 5 | 4 | 7.0 |

## Idea Details

### 1) Cross-platform issue agenda alignment (TV vs Meta vs Google)
- Core question: Are parties/candidate types emphasizing the same issues across TV and digital, or diverging by medium?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- Useful fields: `issue_1..issue_3`, `advertiser_party`, `advertiser_type`, `spent`, `ISSUE*`, `office_corrected`, `party_all`.
- Deliverable: medium-by-party issue heatmaps and divergence indices.
- Key risk: harmonizing issue taxonomies between TV issue names and digital `ISSUE*` codes.

### 2) Geographic targeting congruence
- Core question: Do ads mention places/races that match where they are actually delivered?
- Primary files:
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
- Useful fields: `region_distribution`, `region_distribution_clean`, `entities_states`, `state_matches`, `state_match_binary`, `market`, `station_state`, `election_state`.
- Deliverable: mismatch rate by party/office and maps of spillover targeting.
- Key risk: entity extraction noise in OCR/ASR text.

### 3) Candidate vs group strategy gap
- Core question: How do candidate ads differ from party/issue-group ads in issue focus, tone, and spend?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
  - `analysis/data/raw/digital/2026/sample/Ads2026_Digital_Sample_021226.csv`
- Useful fields: `advertiser_type`, `advertiser_party`, `tone`, `spent`, `issue_*`, `category`.
- Deliverable: strategy profiles by sponsor type and cycle.
- Key risk: 2026 files are samples, so avoid population claims.

### 4) 2024 to 2026 issue shift tracking
- Core question: Which issues gained or lost prominence between 2024 and early 2026 samples?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
- Useful fields: `airdate`, `issue_1..issue_3`, expanded `issue_*` indicators, `advertiser_party`, `category`.
- Deliverable: change-point charts and issue share deltas.
- Key risk: differing issue schema detail between files needs harmonization layer.

### 5) Goal model behavior in digital ads
- Core question: How often do model-assigned goals (Persuade/Donate/GOTV) align with ad context (party, office, spend)?
- Primary files:
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- Useful fields: `goal_*_prediction`, `goal_*_predicted_prob`, `goal_highest_prob`, `spend`, `office_corrected`, `party_all`, `ad_tone`.
- Deliverable: calibration and distribution diagnostics by subgroup.
- Key risk: predictions are model outputs, not ground truth labels.

### 6) Language and outreach segmentation
- Core question: Are Spanish-language or bilingual ads tied to specific issues, parties, or race types?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
  - `analysis/data/raw/digital/2026/sample/Ads2026_Digital_Sample_021226.csv`
- Useful fields: `language`, `issue_spanlang`, `advertiser_party`, `category`, `state`, `market`.
- Deliverable: language-segmented issue/tone profiles and geography.
- Key risk: language metadata quality may differ by medium.

### 7) Tone polarization by party and office
- Core question: How negative is messaging by party, and does tone vary by office/race type?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- Useful fields: `tone`, `ad_tone`, `ad_tone_constructed`, `advertiser_party`, `category`, `office_corrected`.
- Deliverable: tone distribution comparisons and polarization index.
- Key risk: tone definitions may not be fully equivalent across sources.

### 8) Spend efficiency by issue and medium
- Core question: Which issue categories appear most cost-efficient per reach/viewing proxy?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- Useful fields: TV `spent`, `viewers`, `impressions`; digital spend bounds and impression bounds.
- Deliverable: cost-per-1000-style metrics with uncertainty bands.
- Key risk: measurement definitions differ (TV viewers vs platform impressions).

### 9) Market-level saturation and overlap dynamics in TV
- Core question: Where are ad markets most saturated, and how often do campaigns collide in the same windows?
- Primary files:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
- Useful fields: `market`, `daypart`, `program_name`, `callback_start_time`, `callback_end_time`, `overlap`, `spent`, `grps`.
- Deliverable: saturation league tables and temporal overlap plots.
- Key risk: overlap field interpretation may need codebook verification.

### 10) Human-coded vs AI-coded consistency audit
- Core question: How consistent are content/tone/issue signals between legacy human-coded TV schema and newer AI-style schema?
- Primary files:
  - `analysis/data/raw/tv/2024/house_legacy/Ads2024_House_090124-110624_ASR_wmpid_coding_013026.dta`
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.dta`
  - `analysis/data/reference/codebooks/wmp/WMP TV Ads Codebook 2024.pdf`
- Useful fields: legacy `issue_*`, `ad_tone`, `codingstatus`; newer `issue_1..issue_3`, `tone`, `transcript`, `wmp_link`.
- Deliverable: agreement metrics and systematic disagreement patterns.
- Key risk: record linkage may be non-trivial without a guaranteed shared unique key.

## Suggested Starting Picks

1. Cross-platform issue agenda alignment (best balance of value and feasibility).
2. Geographic targeting congruence (strong story and clean operationalization).
3. Candidate vs group strategy gap (fast to execute with clear outputs).
