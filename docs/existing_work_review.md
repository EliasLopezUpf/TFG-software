# Review of Existing Work (as of 2026-11-25)

Audit of the notebooks and outputs present in the repository at commit `e6333c0`. The review was carried out **by reading the notebook code and stored outputs**. The notebooks could **not be re-executed** because the raw data is not in the repository (gitignored).

Severity: 🔴 affects reported numbers · 🟠 affects reproducibility or interpretation · 🟡 cosmetic or minor

---

## Notebook 01 — `01_demographic_analysis.ipynb`

**What it does:** loads the Idescat 2025 census by single year of age (DS-01). It separates single-age rows (sex = total) from municipal totals and validates that the single ages add up to each total (0 mismatches). It then computes 60+ population and % 60+ by municipality, the age-group distribution for Catalonia, a ranking of municipalities ≥5,000 inhabitants by % 60+, and a provisional list of 22 Costa Brava municipalities with charts. Finally it exports two processed CSVs.

### Findings supported by the stored outputs

| Finding | Value | Status |
|---|---|---|
| Catalonia population, 1 Jan 2025 (census) | 8,124,126 | ✅ matches the Idescat release |
| Catalonia 60+ population | 2,106,500 | ✅ (from the `Catalunya` row) |
| Catalonia % 60+ | 25.93 % | ✅ |
| Age structure (shares) | 0-17: 16.68 % · 18-39: 26.75 % · 40-59: 30.64 % · 60-74: 16.05 % · 75-84: 6.85 % · 85+: 3.02 % | ✅ shares are valid, but the **absolute counts in that table are doubled** (see 🔴 issue 1) |
| Highest % 60+ among municipalities ≥5,000 inhabitants | Gironella 33.3 %, Llançà 32.9 %, l'Ametlla de Mar 32.2 %… | ✅ descriptive |
| Costa Brava example values | e.g. Blanes 42,446 / 11,616 / 27.37 %; Colera 489 / 220 / 44.99 % | ✅ consistent with the handover document |

### Issues

1. 🔴 **The `Catalunya` aggregate is treated as a municipality.** The dataset has 948 geographic units: 947 municipalities + `Catalunya`. The notebook never removes the aggregate. As a result:
   - The age-group table (cell 10) sums Catalonia twice. Its "population" column totals 16,248,252 = 2 × 8,124,126, and the 60+ groups total 4,213,000 = 2 × 2,106,500. **The percentages are still correct** (both numerator and denominator are doubled), but the absolute counts must not be quoted.
   - `municipality_stats` and the exported `demographic_municipality_stats_2025.csv` contain a `Catalunya` row. That row then carries into notebook 02 (948 "municipalities").
2. 🟠 **No comarca dimension.** The data only has municipality names, and there is no municipality→comarca mapping. The current primary unit of analysis (comarca) is therefore not yet supported.
3. 🟠 **Joins are by name, not by code.** This is fragile across Idescat exports (articles such as "Escala, l'", renamed or merged municipalities).
4. 🟠 **The title says "Costa Brava"**, but most of the notebook analyses the whole of Catalonia. The Costa Brava list of 22 municipalities has no documented selection criterion (for example, whether inland municipalities such as Mont-ras should count as "Costa Brava" needs a stated rule).
5. 🟠 **Execution order is inconsistent.** Execution counts are not sequential (3, 4, 5, 6, 8, 9, 10, 18, 13, 19, 22…), and the output of cell 1 ("Libraries imported successfully") does not match its source. The notebook has not been verified as running top to bottom.
6. 🟡 The notebook structure required by CLAUDE.md §9 is incomplete: there is no interpretation, limitations or conclusions section.
7. 🟡 `population_by_age_sex_2025.csv` contains only sex = total, despite its name.
8. 🟡 The 60+ threshold is the only one used. 65+ and 75+ are not computed.

## Notebook 02 — `02_socioeconomic_analysis.ipynb`

**What it does:** loads RFDB 2010–2023 (DS-02) and keeps the 2023 per-capita values (provisional). It loads the 2024 ETCA seasonal population (DS-03), merges both with the notebook 01 output by municipality name, and reports coverage (RFDB 49.7 %, ETCA 51.1 % of the 948 units). It checks the ETCA identity and analyses the Costa Brava subset: income vs. 60+ size, seasonal intensity and quarterly profiles. Finally it computes an **"opportunity score"** and exports four processed CSVs.

### Findings supported by the stored outputs

| Finding | Status |
|---|---|
| RFDB 2023 per capita: Catalonia 20,789 €; range 13,633 € (Salt) to 35,425 € (Alella) across 470 municipalities | ✅ matches the Idescat release |
| ETCA identity `ETCA − resident = seasonal total` holds for all municipalities | ✅ |
| 21 of the 22 Costa Brava municipalities have both RFDB and ETCA data (Colera has neither) | ✅ |
| Costa Brava municipalities show positive annual seasonal population, highest relative to residents in el Port de la Selva, Pals, Sant Pere Pescador, Tossa de Mar and Begur | ✅ descriptive |

### Issues

1. 🔴 **The "opportunity score" (cell 18) is an arbitrary composite.** It applies MinMax scaling within 21 municipalities, with subjective weights (60 % size, 20 % share, 20 % income) that are not justified. The ranking depends on the weights and on which municipalities are included (MinMax is relative to the sample). The handover document explicitly says to *avoid arbitrary composite scores*. **Do not use or report it as a finding.** If a prioritisation is needed later, it should come with a weight-sensitivity analysis, or rely on transparent multi-criteria tables instead.
2. 🟠 **Reference years are mixed:** demographics 2025, RFDB 2023 (provisional), ETCA 2024. The notebook does not state this.
3. 🟠 **RFDB is an all-household territorial indicator.** It is not the income of seniors and should not be read as their purchasing power.
4. 🟠 **ETCA covers all ages.** It is not a measure of senior tourism or of seasonal seniors.
5. 🟠 **Coverage is about 50 % of municipalities.** RFDB and ETCA only cover municipalities with ≥1,000 inhabitants. Any comarca aggregation of these indicators must handle the missing small municipalities explicitly (Idescat publishes comarca-level RFDB directly, which is preferable).
6. 🟠 The manual name fix `"Palamós i Sant Joan" → "Palamós"` is not explained. ETCA has a `Codi` column, which could be used instead.
7. 🟠 **There are no markdown cells**: no objective, research questions, interpretation or limitations.
8. 🟡 Cells 15 and 16 are duplicates (cell 15 was never executed).
9. 🟡 Cell 21 uses a relative path `../data/processed` instead of the `PROJECT_ROOT`-based paths defined in cell 0.
10. 🟡 The stored outputs contain the author's local Windows path (cell 0). Consider clearing outputs of personal paths before sharing the repository publicly.
11. 🟡 It uses `scikit-learn` only for MinMax scaling, which is a one-line pandas operation.

## Repository-level issues

- 🟠 **The raw data is not versioned, and no download script or manifest exists**, so the analyses cannot be reproduced from the repository alone.
- 🟠 `requirements.txt` is a full `pip freeze` from Windows. It includes `pywinpty` (Windows-only), which makes `pip install -r requirements.txt` fail on Linux and macOS. The kernel metadata says Python 3.13.3, while the handover says Python 3.12.
- 🟡 `README.md` was empty (now filled in).
- 🟡 The handover document is a `.docx`, which Git cannot diff. Its content is now mirrored in `docs/project_summary.md`.

## Duplicated work

- The Costa Brava municipality list is hard-coded in both notebooks. It should live in a single place, such as a reference CSV or a Python module.
- The seasonal intensity calculation appears three times in notebook 02 (cells 15, 16 and 19).

## Missing analyses (relative to the research priorities)

- Comarca-level demographic sizing (60+, 65+, 75+; absolute and relative).
- Historical demographic trends and official projections.
- Socioeconomic indicators at comarca level and other relevant variables (density, ageing index, dependency, living alone, education, digital use).
- Supply-side inventory (casals, associations, municipal agendas).
- Demand-side research (survey and interviews): design, ethics and sampling.
- Competitor and benchmark review.
- Business model and financial feasibility.
