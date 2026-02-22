# `analysis/data` File Summary

Generated on 2026-02-12 23:35:01 after directory reorganization.

## Recommended Organization (Implemented)

- `raw/`: immutable analysis inputs from providers, grouped by medium (`tv`, `digital`) and year/source.
- `reference/`: codebooks, dictionaries, and course docs that explain fields but are not modeled directly.
- `system/`: non-analytical machine metadata files (for example `.DS_Store`).
- Keep transformations and derived tables outside `raw/` (for example `processed/` and `outputs/`) so source data stays auditable.

## Current Directory Layout

```text
data
├── raw
│   ├── digital
│   │   ├── 2024
│   │   │   ├── google
│   │   │   └── meta
│   │   └── 2026
│   │       └── sample
│   └── tv
│       ├── 2024
│       │   ├── house_legacy
│       │   └── issues_by_creative
│       └── 2026
│           └── sample_with_issues
├── reference
│   ├── codebooks
│   │   ├── adimpact
│   │   │   ├── AdImpact+Data+Dictionary,+Advanced+TV+Data+Suite,+August+2024 (1).docx
│   │   │   └── AdImpact+Data+Dictionary,+Advanced+TV+Data+Suite,+August+2024 (1).pdf
│   │   ├── platforms
│   │   │   ├── 2022 variable description table.xlsx
│   │   │   └── 2024 Meta variable codebook.xlsx
│   │   └── wmp
│   │       ├── CMAGvars_WMP-2022-releasecodebook_v1.0.pdf
│   │       ├── WMP TV Ads Codebook 2024 Human Coding Vars.pdf
│   │       └── WMP TV Ads Codebook 2024.pdf
│   └── course_materials
│       └── Weekly Assignments_Readings SP26.pdf
├── system
│   └── .DS_Store
└── DATA_SUMMARY.md
```

## Scope

- This summary covers every file found under `analysis/data` except this output file (`analysis/data/DATA_SUMMARY.md`) to avoid self-reference.

## Inventory at a Glance

- Total files summarized: 16
- Files in `raw/`: 7
- Files in `reference/`: 8
- Files in `system/`: 1
- Files in `other/`: 0
- `(no extension)`: 1
- `.csv`: 3
- `.docx`: 1
- `.dta`: 2
- `.gz`: 2
- `.pdf`: 5
- `.xlsx`: 2

## Per-File Details

### `analysis/data/raw/digital/2024/google/google2024_set1_20250715.csv.gz`
- Purpose: Compressed 2024 Google ads dataset with spend/impression targeting features.
- Format: GZIP-compressed CSV (`.csv.gz`)
- Size: 57.29 MB (60,070,622 bytes)
- Last modified: 2025-07-15 12:44:46
- Contains: ~2,574,691 data rows after decompression, 92 columns. First columns: ad_id, advertiser_name, advertiser_id, asr_text, ocr_text, ad_url, date_range_start, date_range_end, num_of_days, impressions, first_served_timestamp, last_served_timestamp.
- Notes: Sample first-row values: ad_id=CR01187473623149969409; advertiser_name=TIM SHEEHY FOR MONTANA; advertiser_id=AR00090566463542263809; asr_text=as your Senator I'll fight to protect and expand access to our public lands because public lands bel...; ocr_text=PROTECT PUUC LNDS PROTECT PUHC LANDS PAID FOR BY TIM SHEEHY FOR MONTANA APPROVED BY TIM SHEHY PAID F...; ad_url=https://adstransparency.google.com/advertiser/AR00090566463542263809/creative/CR01187473623149969409...

### `analysis/data/raw/digital/2024/meta/meta2024_set1_20250714.csv.gz`
- Purpose: Compressed 2024 Meta ads dataset with modeling/entity features.
- Format: GZIP-compressed CSV (`.csv.gz`)
- Size: 358.85 MB (376,280,213 bytes)
- Last modified: 2025-09-18 10:32:12
- Contains: ~3,575,204 data rows after decompression, 109 columns. First columns: ad_id, fbid, page_id, page_name, funding_entity, pd_id, ad_creative_body, ad_creative_link_title, ad_creative_link_description, ad_creative_link_caption, ad_delivery_start_time, first_day_active.
- Notes: Sample first-row values: ad_id=x_1000012438450011; fbid=1000012438450010; page_id=328078757051975; page_name=Ron Odenthal; funding_entity=Odenthal4MO; pd_id=pd-328078757051975-1

### `analysis/data/raw/digital/2026/sample/Ads2026_Digital_Sample_021226.csv`
- Purpose: Sample digital political ads dataset (cross-platform fields).
- Format: CSV (comma-separated text)
- Size: 10.37 MB (10,876,028 bytes)
- Last modified: 2026-02-12 15:35:28
- Contains: ~25,392 data rows, 27 columns. First columns: advertiser_type, advertiser_party, advertiser, title, advertiser_id, state, election, link, market, media_type, race, station.
- Notes: Sample first-row values: advertiser_type=Issue Group; advertiser_party=Republican; advertiser=Bucks County Republican Committee; title=Vote Jen Schorn for District Attorney; advertiser_id=263622; state=PA

### `analysis/data/raw/tv/2024/house_legacy/Ads2024_House_090124-110624_ASR_wmpid_coding_013026.dta`
- Purpose: Legacy/older-provider TV ad dataset for House races, stored in Stata format.
- Format: Stata Data File (binary, release 118)
- Size: 2.55 GB (2,743,407,191 bytes)
- Last modified: 2026-01-30 11:31:31
- Contains: 932,992 rows (metadata), 452 variables. First variables: alt, creative, asr_text, wmpid, cand_id, weslink, market2010, nielsendmaid, sponsor, category, categorystate, l.

### `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.csv`
- Purpose: Large TV ad dataset with issue coding by creative/ad airing records.
- Format: CSV (comma-separated text)
- Size: 1.02 GB (1,091,820,245 bytes)
- Last modified: 2026-01-30 11:27:03
- Contains: ~942,763 data rows, 66 columns. First columns: advertiser_party, advertiser_type, advertiser, airdate, election_state, election, issue_1, issue_2, issue_3, market, spent, grps.
- Notes: Sample first-row values: advertiser_party=Democrat; advertiser_type=Candidate; advertiser=Titus for NV CD-01; airdate=2024-09-13; election_state=NV; election=NV CD-01 2024 General

### `analysis/data/raw/tv/2024/issues_by_creative/Ads2024_IssuesbyCreative_090124-110624_HSE_AI_013026.dta`
- Purpose: Large TV ad dataset with issue coding by creative/ad airing records.
- Format: Stata Data File (binary, release 118)
- Size: 1.92 GB (2,059,979,950 bytes)
- Last modified: 2026-01-30 11:32:58
- Contains: 942,763 rows (metadata), 66 variables. First variables: advertiser_party, advertiser_type, advertiser, airdate, election_state, election, issue_1, issue_2, issue_3, market, spent, grps.

### `analysis/data/raw/tv/2026/sample_with_issues/Ads2026_withissues_Sample_021226.csv`
- Purpose: Sample TV ad airing dataset with engineered issue indicator fields.
- Format: CSV (comma-separated text)
- Size: 84.48 MB (88,585,377 bytes)
- Last modified: 2026-02-12 15:34:04
- Contains: ~61,696 data rows, 150 columns. First columns: advertiser_party, advertiser_type, advertiser, airdate, election_state, election, issue_1, issue_2, issue_3, market, spent, grps.
- Notes: Sample first-row values: advertiser_party=Independent; advertiser_type=Candidate; advertiser=Williams for Orleans Parish Tax Assessor; airdate=2025-10-03; election_state=LA; election=Orleans Parish Tax Assessor 2025 Primary

### `analysis/data/reference/codebooks/adimpact/AdImpact+Data+Dictionary,+Advanced+TV+Data+Suite,+August+2024 (1).docx`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: Microsoft Word `.docx` (Office Open XML)
- Size: 430.89 KB (441,227 bytes)
- Last modified: 2026-02-12 23:15:43
- Contains: Text-based data dictionary document. Opening text: CONFIDENTIAL Ad Viewings | TV Ad-Viewing Data Each row in the dataset represents an ad-viewing event, where automated content recognition technology identifies a specific advertisement on an individual television. The data spans ad-viewings from January 2022 to the present, with new viewings becoming accessible within 24 hours of occurrence. The following fields combine information about the ad-viewing with metadata collected about the associated program, television, creative, and other internally curated entities. All viewings are gathered by finding ACR matches to fingerprints of AdImpact’s ...

### `analysis/data/reference/codebooks/adimpact/AdImpact+Data+Dictionary,+Advanced+TV+Data+Suite,+August+2024 (1).pdf`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: PDF document
- Size: 411.83 KB (421,719 bytes)
- Last modified: 2026-02-12 23:15:38
- Contains: 11 pages. Opening text indicates: CONFIDENTIAL AdImpact reserves the authority to change or amend the fields included for any reason. Users should anticipate new fields being added in the future for any reason. Last Revised: August 1, 2024 Ad Viewings | TV Ad-Viewing Data Each row in the dataset represents an ad-viewing event, where automated content recognition technology identifies a specific advertisement on an individual television. The data spans ad-viewings from January 2022 to the present, with new viewings becoming accessible within 24 hours of occurrence. The following fields combine information about the ad-viewing w...

### `analysis/data/reference/codebooks/platforms/2022 variable description table.xlsx`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: Microsoft Excel `.xlsx` workbook
- Size: 12.65 KB (12,956 bytes)
- Last modified: 2025-10-10 08:31:34
- Contains: Workbook with sheets: tab_data.
- Notes: First-sheet preview rows: Variable, Description, Data source | ad_id, unique identifier of ads, Meta, Google | page_id, identifier of page names, Meta | page_name, page name of the ad sponsor (Meta), Meta

### `analysis/data/reference/codebooks/platforms/2024 Meta variable codebook.xlsx`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: Microsoft Excel `.xlsx` workbook
- Size: 13.64 KB (13,964 bytes)
- Last modified: 2025-11-19 12:21:32
- Contains: Workbook with sheets: WIP.
- Notes: First-sheet preview rows: Variable, Description, exist_in_file | ad_id, unique identifier of ads, 1.0 | page_id, identifier of page names, 1.0 | page_name, page name of the ad sponsor (Meta), 1.0

### `analysis/data/reference/codebooks/wmp/CMAGvars_WMP-2022-releasecodebook_v1.0.pdf`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: PDF document
- Size: 498.34 KB (510,297 bytes)
- Last modified: 2026-02-05 13:58:44
- Contains: 17 pages. Opening text indicates: Political Advertising in 2022 Wesleyan Media Project Release Version 1.0 (August 2025) This collection provides detailed tracking data on when and where political ads aired during the 2022 elections. It covers all broadcast television stations in all media markets in the United States. Ads aired in U.S. Senate, U.S. House and gubernatorial races are also coded for their content. DATABASES The data collection comes in four different files: 1. wmp-senate-2022: contains information on all ads aired in U.S. Senate races 2. wmp-house-2022: contains information on all ads aired in U.S. House races 3...

### `analysis/data/reference/codebooks/wmp/WMP TV Ads Codebook 2024 Human Coding Vars.pdf`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: PDF document
- Size: 261.27 KB (267,542 bytes)
- Last modified: 2026-02-05 14:00:38
- Contains: 9 pages. Opening text indicates: Wesleyan Media Project Codebook – 2024 Supplemental Guide CREATIVE TITLE [Please display CMAG-attributed name of ad at top of page] GOAL In your judgment, what are the goals of the ad? (Select all goals of the ad. Select one primary goal. Check only one box per row.) Goals Not referenced Goal Primary Goal 0 1 2 To persuade people to vote for or against a candidate To convince viewers to donate money To gather more information about the viewer (e.g., “sign up,” “learn more”) or to encourage viewers to become more involved in the campaign To ask the viewer to contact a legislator about an issue ...
- Notes: Likely duplicate content: same file size as `reference/codebooks/wmp/WMP TV Ads Codebook 2024.pdf`.

### `analysis/data/reference/codebooks/wmp/WMP TV Ads Codebook 2024.pdf`
- Purpose: Reference documentation describing variables, coding rules, or data schema.
- Format: PDF document
- Size: 261.27 KB (267,542 bytes)
- Last modified: 2026-02-12 23:12:45
- Contains: 9 pages. Opening text indicates: Wesleyan Media Project Codebook – 2024 Supplemental Guide CREATIVE TITLE [Please display CMAG-attributed name of ad at top of page] GOAL In your judgment, what are the goals of the ad? (Select all goals of the ad. Select one primary goal. Check only one box per row.) Goals Not referenced Goal Primary Goal 0 1 2 To persuade people to vote for or against a candidate To convince viewers to donate money To gather more information about the viewer (e.g., “sign up,” “learn more”) or to encourage viewers to become more involved in the campaign To ask the viewer to contact a legislator about an issue ...
- Notes: Likely duplicate content: same file size as `reference/codebooks/wmp/WMP TV Ads Codebook 2024 Human Coding Vars.pdf`.

### `analysis/data/reference/course_materials/Weekly Assignments_Readings SP26.pdf`
- Purpose: Course/lab assignment instructions and reading checklist.
- Format: PDF document
- Size: 68.62 KB (70,269 bytes)
- Last modified: 2026-02-12 23:10:42
- Contains: 2 pages. Opening text indicates: HOMEWORK ASSIGNMENTS: WEEK 3: (1) Post your weekly goals to Slack by Friday, Feb 6 (ideally before you leave the lab!) (2) Continue exploring data: (a) TV datasets (i) older data provider -- labeled Ads2024_House... (ii) newer data provider, which is labeled with an "AI" in the title -- Ads2024_Issues… (b) New additions to the folder (i) WMP-processed digital data for 2024 Meta & 2024 Google (2022 data for both platforms is publicly available too if you’d like it) (ii) Upcoming: sample of 2026 data (5%), which won’t be limited to US House 1) 2026 TV sampled by category 2) 2026 digital sampled ...

### `analysis/data/system/.DS_Store`
- Purpose: macOS Finder metadata file; not analytical data.
- Format: Apple `.DS_Store` binary metadata file
- Size: 6.00 KB (6,148 bytes)
- Last modified: 2026-02-12 23:17:22
- Contains: Desktop/Finder view settings for this folder.

## Observations

- Most storage is in a small set of large, row-level ad tables under `raw/` (`.csv`, `.dta`, `.csv.gz`).
- Documentation files under `reference/` are now isolated from analysis inputs, reducing accidental joins/imports.
- Two WMP codebook PDFs under `reference/codebooks/wmp/` appear to be duplicates by size and extracted text prefix.