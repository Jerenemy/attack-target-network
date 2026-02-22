# NLP Project Ideas for `analysis/data`

Scoring scale: 1-10 (10 is best).
- Feasibility: practical with current files and moderate coding effort
- Impact: substantive value for understanding political ad strategy
- Interestingness: how compelling the core question is
- NLP Leverage: how central NLP is (vs basic tabulation)
- Publishability: likelihood of yielding a clean, defensible story
- Overall: weighted project quality score

## Ranked Idea Table

| Rank | Idea | Feasibility | Impact | Interestingness | NLP Leverage | Publishability | Overall |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | CTA language extraction and goal consistency audit | 9 | 9 | 8 | 8 | 9 | 8.7 |
| 2 | Policy vs identity framing classifier by party/office | 8 | 9 | 9 | 9 | 8 | 8.6 |
| 3 | Attack-target network from named entities in ad text | 7 | 9 | 9 | 9 | 8 | 8.4 |
| 4 | Message repetition and slogan recycling across markets | 8 | 8 | 8 | 8 | 8 | 8.0 |
| 5 | OCR vs ASR disagreement as an ad-format/quality signal | 8 | 7 | 8 | 9 | 7 | 7.9 |
| 6 | Emotion lexicon profiling (fear/anger/hope) by issue | 8 | 8 | 8 | 8 | 7 | 7.9 |
| 7 | Topic drift from 2024 to 2026 in TV transcripts | 8 | 8 | 7 | 8 | 7 | 7.7 |
| 8 | Spanish vs English framing differences | 7 | 8 | 8 | 8 | 7 | 7.6 |
| 9 | Candidate style fingerprinting (readability, complexity, directness) | 7 | 7 | 8 | 8 | 7 | 7.4 |
| 10 | Cross-platform narrative portability (Meta vs Google vs TV) | 6 | 8 | 8 | 9 | 7 | 7.3 |

## Detailed Ideas

### 1) CTA language extraction and goal consistency audit
- Core question: Does explicit call-to-action language in text match predicted goals (`DONATE`, `GOTV`, `PERSUADE`)?
- Data to use:
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- NLP method: regex + phrase dictionary + lightweight text classifier for CTA intent phrases.
- Why this is interesting: It tests whether modeled goals align with what ads literally ask viewers to do.
- Expected result: high match for explicit verbs (`donate`, `vote`, `register`) and lower confidence in generic persuasion text.
- Why it is worth your time: Fast to execute, strong interpretability, and immediately useful for trusting downstream goal analyses.

### 2) Policy vs identity framing classifier by party/office
- Core question: Are campaigns winning attention via policy argumentation or identity/character framing?
- Data to use:
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
- NLP method: supervised or weakly supervised frame classifier (policy/program vs identity/personality/values).
- Why this is interesting: It captures campaign style, not just issue topic, which is a deeper strategic dimension.
- Expected result: policy-heavy framing in some offices/issues, identity framing stronger in attack-heavy contexts.
- Why it is worth your time: Produces a reusable feature for many future projects and can support a publishable narrative.

### 3) Attack-target network from named entities in ad text
- Core question: Who is being mentioned/attacked most, and how does that network vary by party and office?
- Data to use:
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
- NLP method: NER + co-mention graph + sentiment/tone attachment.
- Why this is interesting: Turns ad discourse into a strategic interaction map instead of isolated ad records.
- Expected result: a small number of high-centrality national figures plus localized target clusters by race/market.
- Why it is worth your time: Graph outputs are compelling, interpretable, and often presentation/publication friendly.

### 4) Message repetition and slogan recycling across markets
- Core question: How much text is reused verbatim or near-verbatim across places and sponsors?
- Data to use:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
- NLP method: MinHash/LSH or embedding similarity clustering over transcript/OCR text.
- Why this is interesting: Distinguishes centralized messaging campaigns from localized tailoring.
- Expected result: high reuse for national/group campaigns, more customization in local races.
- Why it is worth your time: Helps explain media strategy efficiency and can guide future deduplication in your pipeline.

### 5) OCR vs ASR disagreement as an ad-format/quality signal
- Core question: When visual text and spoken text diverge, what strategies are being used?
- Data to use:
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz` (both `ocr_text` and `asr_text` are dense)
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz` (`ocr_text` + creative body)
- NLP method: semantic similarity between OCR and ASR; disagreement clustering.
- Why this is interesting: Reveals whether campaigns rely on visual disclaimers, emotional imagery text, or spoken persuasion.
- Expected result: some ad types show intentional divergence (e.g., visual legal/policy text vs emotive spoken narration).
- Why it is worth your time: New angle that leverages multimodal text artifacts you already have without extra data collection.

### 6) Emotion lexicon profiling (fear/anger/hope) by issue
- Core question: Which issues are framed with fear, anger, or optimism, and by whom?
- Data to use:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
- NLP method: lexicon + transformer-based emotion tagging (small validation subset recommended).
- Why this is interesting: Emotion is central to persuasion and often more explanatory than topic alone.
- Expected result: fear/anger concentration in crime/immigration-style messaging and optimism in self-promotional ads.
- Why it is worth your time: High communication value and useful for both descriptive and predictive follow-up work.

### 7) Topic drift from 2024 to 2026 in TV transcripts
- Core question: How did messaging themes shift from 2024 TV ads to the 2026 sample?
- Data to use:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
- NLP method: dynamic topic modeling or BERTopic over transcripts by month/quarter.
- Why this is interesting: Captures agenda evolution and whether new narratives displaced old ones.
- Expected result: persistence of core issues plus emergence of new narrative clusters in 2026 sample.
- Why it is worth your time: Strong temporal story with clear visuals and direct relevance for campaign-cycle comparisons.

### 8) Spanish vs English framing differences
- Core question: Do Spanish-language ads use distinct frames, sentiment, or call-to-action patterns?
- Data to use:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
- NLP method: language detection validation + bilingual keyword/frame analysis.
- Why this is interesting: Tests whether multilingual outreach is substantive tailoring vs direct translation.
- Expected result: partial overlap on major issues but differing frame emphasis and tone.
- Why it is worth your time: Policy-relevant and under-explored; can generate concrete findings with manageable scope.

### 9) Candidate style fingerprinting (readability, complexity, directness)
- Core question: Are some sponsors consistently using simpler or more direct language, and does it correlate with spend/outcomes proxies?
- Data to use:
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- NLP method: readability metrics, sentence complexity, pronoun and imperative usage.
- Why this is interesting: Provides a quantifiable communication-style profile per sponsor/party/office.
- Expected result: simpler imperative-heavy language in mobilization/fundraising contexts.
- Why it is worth your time: Low engineering cost and easy to integrate as controls in future models.

### 10) Cross-platform narrative portability (Meta vs Google vs TV)
- Core question: Which narrative templates survive across platform constraints and which are medium-specific?
- Data to use:
  - `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
  - `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
  - `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
- NLP method: sentence embeddings + nearest-neighbor transfer analysis by issue and tone.
- Why this is interesting: It directly answers whether messaging architecture is channel-agnostic or channel-native.
- Expected result: high portability for broad persuasion templates, lower portability for CTA-heavy digital variants.
- Why it is worth your time: Strategic insight for campaign communication planning and for your own cross-media research design.

## Recommended First 3 NLP Projects

1. CTA language extraction and goal consistency audit.
2. Policy vs identity framing classifier by party/office.
3. Message repetition and slogan recycling across markets.
