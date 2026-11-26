# Research Log

Chronological record of research work. Newest entries at the bottom. Each entry: date, what was done, outcome, open questions.

---

## 2026-10-29 — Project set-up and demographic analysis (author)
*Reconstructed from the Git history (commits `60a4f4e`, `b871794`).*

- Created the initial repository structure (`data/raw`, `data/processed`, `notebooks`, `reports`).
- Notebook 01: loaded the Idescat 2025 census by single year of age. Validated that the single ages sum to the totals, computed 60+ by municipality, built the age-group distribution, and drew up a provisional Costa Brava list (22 municipalities).

## 2026-10-30 — Socioeconomic and seasonal context (author)
*Reconstructed from commit `33eb173`.*

- Notebook 02: RFDB per capita 2023 (provisional) and ETCA seasonal population 2024. Merged by municipality name, analysed coverage, ran a Costa Brava case study, and built an exploratory "opportunity score".

## 2026-11-25 — Scope update and handover (author)
*Commit `e6333c0`.*

- Following tutor guidance, the scope moved from the Costa Brava to **Catalonia with comarques as the primary unit**. 60+ was kept as a provisional threshold.
- Added `CLAUDE.md` and the handover document `docs/TFG_Project_Summary_Claude_Code_Handover.docx`.

## 2026-11-25 — Repository audit and documentation (Claude Code)

**Goal:** understand the existing work and prepare the repository for autonomous research. No new analysis was carried out.

**Done:**
- Inspected all files, the Git history, both notebooks (code and stored outputs) and the handover document.
- Checked key notebook figures against Idescat releases (census total 8,124,126; RFDB 2023 extremes; ETCA and RFDB coverage rules).
- Wrote the audit `docs/existing_work_review.md`.
- Created or updated `README.md`, `CLAUDE.md`, `docs/project_summary.md`, `docs/research_log.md`, `docs/decisions_log.md`, `docs/data_sources.md` and `docs/market_study_progress.md`.

**Key findings of the audit:**
- The `Catalunya` aggregate row is treated as a municipality in notebook 01. The absolute counts in the age-group table are doubled (the shares are unaffected), and the row carries into the processed files and notebook 02.
- The "opportunity score" in notebook 02 uses arbitrary weights and should not be reported.
- The raw data is not in Git and has no download manifest, so the work is not reproducible from the repository.
- There is no comarca dimension yet, and joins are by municipality name.

**Limitations of this audit:** the notebooks were not re-executed (no data available in the container). The findings are based on code and stored outputs.

**Open questions:** raw-data versioning policy (D-004), whether to fix notebooks 01 and 02 in place or supersede them (D-005), and the repository structure (D-006).

## 2026-11-26 — Comarca-level datasets received and validated (Claude Code)

**Done:**
- The author uploaded three Idescat comarca-level files: 2025 census by five-year age group and sex, 2023 RFDB (provisional), and 2024 ETCA by quarter. They are stored unmodified in `data/raw/comarca/` with SHA-256 checksums and registered as DS-04 to DS-06 in `docs/data_sources.md`.
- Structural validation: no duplicates or missing values (apart from the Catalonia ETCA row), age and sex subtotals are consistent, and the comarques reconcile with the Catalonia totals in all three files. Territorial names are identical across the files (43 units).

**Observations:**
- Comarca RFDB has full coverage. This addresses the roughly 50 % municipal coverage problem in notebook 02.
- The five-year age groups allow exact 60+, 65+ and 75+ aggregates.
- The ETCA file's resident population (8,012,231) differs from the 2025 census (8,124,126). The two must not be mixed as denominators.

**Pending:** the download URLs and dates were not recorded by the author. The ETCA reference year was taken from the author's description, not from the file. No historical series or projections have been obtained yet.

## 2026-11-26 — Notebook 03: senior population by comarca (Claude Code)

**Goal:** comarca-level demographic sizing (60+, 65+, 75+): size, concentration, threshold sensitivity, trends, projections and socioeconomic context.

**Data work:**
- Wrote `scripts/download_idescat.py` (Idescat Tables API v2, JSON-stat), with a manifest of URLs, times and SHA-256. Downloaded the census by comarca (2011, 2021–2025), the census by municipality (same years), the comarca population estimates (2012–2025), the base-2024 projections (three scenarios) and the municipality → comarca code list (DS-07 to DS-11).
- Discarded approach: municipal population estimates (`ep`) give age detail for only 25 municipalities before 2021. The download was replaced by the municipal census, which is complete for 2011 and 2021–2025.
- Found that the Idescat code list already applies Llei 7/2025 (Aiguafreda: Vallès Oriental → Osona). This was reverted to the 1 Jan 2025 division (D-011). The rebuilt comarques then match the published 2024–2025 tables exactly. In 2011 and 2021–2023 the only differences are the documented boundary changes (Moianès, Lluçanès, Biosca and Torà) plus rounding in the 2011 census.
- Reusable code in `src/tfg/`: JSON-stat reader, paths, territorial mapping.
- Raw data is now versioned (D-004 adopted).

**Main results** (facts; details and caveats in the notebook):
- 1 Jan 2025: 2,106,500 residents aged 60+ (25.93 %), 1,601,987 aged 65+ (19.72 %) and 802,324 aged 75+ (9.88 %).
- Concentration: 3 comarques hold 51 % of all 60+ residents, 10 hold 76 %, and Barcelonès alone 30 %. Shares range from 22.1 % (Gironès) to 36.5 % (Terra Alta). Size vs share: Spearman −0.58.
- Rankings are robust to the threshold: size ρ ≥ 0.998; share ρ = 0.92–0.98; top 10 overlap 9–10 of 10.
- 2021→2025 (constant boundaries): 60+ +169,362 (+8.7 %) against +4.8 % for the total population. 60+ grew in all 43 comarques, and its share rose in 42 (not in Barcelonès). Growth was fastest in the metropolitan ring and coastal comarques, and slowest in the most aged ones (share vs growth: ρ = −0.70).
- Projections 2025→2040: 60+ +31 % (low), +36 % (medium) and +42 % (high). Growth is positive in every comarca and scenario. Medium scenario: 2.87 M aged 60+ (32.9 %) in 2040.
- Context (descriptive): RFDB is ρ = 0.39 with size and ρ = −0.34 with share. ETCA is essentially unrelated to share (ρ = 0.18).

**Limitations:** population ≠ demand; methodological break in the 2011 census; projections are scenarios; residents only (seasonal seniors are not captured); context indicators are not age-specific.

**Open questions for the tutor:** primary threshold; reference projection scenario (D-014); selection of comarques for fieldwork.

## 2026-11-26 — Notebook 04: context, territorial profiles and fieldwork candidates (Claude Code)

**Goal:** add context to the comarca analysis (living alone, urbanisation, socioeconomic level, education, digital use), group comarques into transparent profiles, and propose fieldwork comarques.

**Data work:**
- Extended `scripts/download_idescat.py` with DS-12 to DS-16: census household and education indicators, degree of urbanisation, the IST socioeconomic index, and the ICT household survey 2025.
- Added `tfg.idescat.read_idescat_html_tables` to parse Idescat's table exports.
- Rejected approach: rebuilding "75+ living alone" from municipalities. Suppression in 486 small municipalities biased rural comarques by up to 2.6 pp, so the published 2021 comarca values are used, with boundary flags (D-017).
- Urbanisation rebuilt from municipalities matches the comarca table and the 2025 census exactly.
- Searched for digital use by age below Catalonia level, and for people aged 75+: none found in Idescat or INE tables. The ICT survey covers ages 16–74 for Catalonia as a whole.

**Main results:**
- 28.1 % of people aged 75+ live alone (2021), about 205,000. The share ranges from 18.4 % (Terra Alta) to 33.4 % (Pallars Jussà); Barcelonès is 31.1 % (about 78,000). It is unrelated to rurality or senior share (|ρ| ≤ 0.18).
- Senior size tracks density (ρ = 0.91) and urbanisation (ρ = −0.90 with % rural). Senior share tracks rurality (ρ = 0.66). The IST (83–107) is unrelated to senior size or share.
- Ages 65–74 (Catalonia 2025): 92.7 % used the internet in the last 3 months and 90.2 % use it weekly, but only 36.1 % bought online, against 69–76 % for ages 25–54.
- Five rule-based profiles (D-016). P1 Large, non-seasonal: 11 comarques, 76.5 % of all seniors. P2 Seasonal, medium/large: 6, 11.3 %. P3 Seasonal, small: 4, 0.5 %. P4 Aged and rural: 10, 3.0 %. P5 Intermediate: 12, 8.7 %. Threshold changes reassign 0–6 comarques.
- Proposed fieldwork comarques (D-018): Vallès Occidental (alt. Barcelonès), Baix Empordà (alt. Selva), Berguedà (alt. Terra Alta), with contrasting municipal structures.

**Hypotheses raised:** H4 (online transaction, not access, is the digital barrier for 65–74); H5 (people 75+ living alone concentrated in Barcelona); H6 (rural supply less visible online).

**Correction:** the NB02 name fix "Palamós i Sant Joan" → "Palamós" reflects a municipal rename (noted in `existing_work_review.md`).
