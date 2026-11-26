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
