# Data Sources

Registry of every dataset used or evaluated in the project. One entry per dataset.

**Status legend:** ✅ verified against the source · ⚠️ to verify · ❌ unknown

> **Important:** `data/raw/` and `data/processed/` are listed in `.gitignore`, so **no data file is in the Git repository**. The files below exist only on the author's local machine. To reproduce the analyses you have to download them again from the sources listed. Recording exact download URLs, dates and checksums is still pending (see "Open actions" at the end).

---

## DS-01 — Population by sex and single year of age, municipalities (2025)

| Field | Value |
|---|---|
| Local file | `data/raw/censph_10_mun_2025_pc.csv` |
| Producer | Idescat (Institut d'Estadística de Catalunya) |
| Statistical operation | *Cens de població i habitatges* (annual census, code `censph`) ✅ (inferred from the filename prefix `censph` and checked against the Idescat catalogue) |
| Table | Population by sex and single year of age (*any a any*), all municipalities ⚠️ (exact table/URL not recorded) |
| Reference date | 1 January 2025 ✅ (Catalonia total 8,124,126 matches the Idescat release) |
| Publication date | 2 December 2025 (census release on population by sex) ⚠️ to confirm for this specific file |
| Download date | ❌ not recorded (before 29 Oct 2026, the first commit of notebook 01) |
| Geographic granularity | Municipality (947 municipalities) + one aggregate row `Catalunya` |
| Format | CSV (Spanish-language export), 290,088 rows × 7 columns: `año, municipio, edad, sexo, concepto, estado, valor` |
| Age coding | `"0 años"` … `"100 años y más"` (open-ended top category) + `"total"` |
| Sex coding | `hombres`, `mujeres`, `total` |
| Identifiers | Municipality **name only**: no INE/Idescat code. Joins are by name. |
| `estado` column | Entirely empty |
| Licence | Idescat general reuse terms: reuse allowed with attribution, without distortion, citing the date of the last update. The Idescat services catalogue describes CC BY as the default licence. ⚠️ to confirm for this table |
| Used in | `notebooks/01_demographic_analysis.ipynb` |
| Notes | The census figures are Idescat's reference population figures and **differ from the Padró municipal d'habitants**. Do not mix the two sources without stating which one you use. Idescat also publishes this census table at comarca level, which could replace a municipality→comarca aggregation (to evaluate). |

Validation done in notebook 01: the sum of the single-age rows equals the official total in all 948 geographic units (0 mismatches). There are no duplicate rows.

## DS-02 — Household gross disposable income (RFDB), municipalities (2010–2023)

| Field | Value |
|---|---|
| Local file | `data/raw/rfdb_municipalities.csv` |
| Producer | Idescat. Statistical operation *Renda familiar disponible bruta territorial* (`rfdbc`) ✅ |
| Indicators | `valor (miles €)`, `por habitante (€)`, `por habitante (índice Cataluña=100)` |
| Reference period | 2010–2023 (annual). **2023 is provisional** (`estado = p`) ✅ |
| Coverage | Municipalities with more than 1,000 inhabitants (current series, statistical revision 2024): 470 municipalities in 2023 + Catalunya ✅ |
| Format | CSV `;`-separated, decimal comma in the index indicator, 19,782 rows × 6 columns |
| Identifiers | Name only |
| Download date | ❌ not recorded |
| Licence | Idescat general reuse terms (see DS-01) ⚠️ |
| Used in | `notebooks/02_socioeconomic_analysis.ipynb` (2023, per capita only) |
| Notes | This is a **territorial, all-household** indicator. It is not the income of people aged 60+. Older series (bases 2008 and earlier) used a 5,000-inhabitant threshold, so long time series have coverage breaks. Notebook values were checked against the Idescat 2023 release: highest Alella 35,425 €, lowest Salt 13,633 €, Catalonia 20,789 € ✅. |

## DS-03 — Seasonal population estimates (ETCA), municipalities, quarterly (2024)

| Field | Value |
|---|---|
| Local file | `data/raw/seasonal_population_quarterly.csv` |
| Producer | Idescat. Statistical operation *Estimacions de població estacional* (`epe`) ✅ |
| Content | Seasonal ETCA population by quarter (T1–T4) and annual total, resident population, ETCA population |
| Reference period | 2024 ⚠️ (inferred from the notebook's variable names; confirm in the file header) |
| Coverage | Since 2021: municipalities with ≥1,000 residents or ETCA population (until 2020: >5,000 + comarca capitals) ✅. The file has 485 rows (484 municipalities + Catalunya). |
| Format | CSV (Catalan export) with 7 metadata lines before the header; `..`/`...` = missing |
| Identifiers | `Codi` (6-digit municipal code) + `Nom` |
| Download date | ❌ not recorded |
| Licence | Idescat general reuse terms ⚠️ |
| Used in | `notebooks/02_socioeconomic_analysis.ipynb` |
| Definitions | 1 ETCA = one person present for a full year (one person-day = 1/365). Seasonal population = non-resident inflows − resident outflows. ETCA population = residents + non-residents present − residents absent ✅ |
| Notes | Measures **population load** and covers all ages: it is **not** a senior-tourism indicator. Idescat warns of methodological breaks, including a 2022 improvement. Notebook check: `ETCA − resident = seasonal total` for all municipalities ✅. One manual name harmonisation is applied (`"Palamós i Sant Joan" → "Palamós"`), ⚠️ to verify using codes. |

---

## Comarca-level datasets (received 2026-11-26)

The author downloaded these three files from Idescat and uploaded them on 2026-11-26. They are stored unmodified in `data/raw/comarca/`, using the original Idescat filenames without the upload prefix. All three cover **43 territorial units (42 comarques + Aran)** plus one aggregate `Catalunya`/`Cataluña` row, and the territorial names are identical across the three files. The set includes Lluçanès, a recently created comarca, which matters for historical series (comarca boundaries change over time).

### DS-04 — Population by sex and five-year age group, comarques (2025)

| Field | Value |
|---|---|
| Local file | `data/raw/comarca/censph-539-5976-com.csv` |
| SHA-256 | `1127d045f5fd392aa27eb3aee4702ca168778069552695fd10efdd42a0b84d60` |
| Producer / operation | Idescat, *Cens de població i habitatges* (`censph`), table 539 "Població. Per sexe i edat quinquennal" ✅ |
| URL | https://www.idescat.cat/pub/?id=censph&n=539 (comarca breakdown) ⚠️ exact download URL not recorded |
| Reference date | 1 January 2025 |
| Granularity | Comarca + Catalunya |
| Format | CSV `;`, UTF-8 with BOM, Catalan labels. 2,904 rows × 7 columns: `any, comarca o Aran, edat quinquennal, sexe, concepte, estat, valor` |
| Age coding | 20 five-year groups `de 0 a 4 anys` … `de 95 a 99 anys`, `100 anys o més`, `total`. The 60+, 65+ and 75+ thresholds can be derived exactly. |
| Sex coding | `homes`, `dones`, `total` |
| Licence | Idescat reuse terms (attribution) ⚠️ |
| Validation (2026-11-26) | 0 duplicates, 0 missing values. Age groups sum to the totals for every territory, and men + women = total in every cell. **The 43 comarques sum exactly to Catalunya (8,124,126) for every age group.** Catalonia 60+ = 2,106,500 (25.93 %), consistent with DS-01. |

### DS-05 — Household gross disposable income (RFDB), comarques (2023, provisional)

| Field | Value |
|---|---|
| Local file | `data/raw/comarca/rfdbc-21181-25017-com.csv` |
| SHA-256 | `6a6c3635a816b8fb09fc0de65f6028a648a5a75054069d4948a03e974ac0cc73` |
| Producer / operation | Idescat, *Renda familiar disponible bruta territorial* (`rfdbc`) ✅ |
| URL | https://www.idescat.cat/pub/?id=rfdbc (comarca table) ⚠️ exact download URL not recorded |
| Reference period | 2023. **All values are provisional** (`estat = p`). |
| Indicators | `valor (milers €)`, `per habitant (€)`, `per habitant (índex Catalunya=100)` |
| Format | CSV `;`, UTF-8 with BOM, **decimal comma** (read with `decimal=","`). 132 rows × 6 columns. |
| Licence | Idescat reuse terms ⚠️ |
| Validation (2026-11-26) | The comarques' total RFDB sums to 165,424,079 k€ against the Catalunya figure of 165,424,076 k€ (a difference of 3 k€, consistent with rounding). Per capita ranges from 15,287 € (Montsià) to 23,632 € (Barcelonès); Catalonia is 20,789 €. **Full coverage of all comarques**, unlike the municipal file (DS-02). |
| Notes | All-household territorial income, not the income of seniors. |

### DS-06 — Seasonal population ETCA by quarter, comarques (2024)

| Field | Value |
|---|---|
| Local file | `data/raw/comarca/idescat-aec-15960-1.csv` |
| SHA-256 | `8cb11ad5989be40970e15bf7abc24bcb9ac301deac70da4c0ce8515f94326d1b` |
| Producer / operation | Idescat, *Anuari estadístic de Catalunya* table 15960, "Estimaciones de población estacional (base 2021). Por trimestres. Comarcas y Aran" (source operation: `epe`) ✅ |
| URL | https://www.idescat.cat/indicadors/?id=aec&n=15960 ⚠️ exact download URL not recorded |
| Reference period | 2024 (as stated by the author when uploading) ⚠️ the file itself contains no year column |
| Format | CSV `;`, UTF-8 with BOM, **long "row/col" layout** (`row; col; r; c; value; status`), Spanish labels, decimal comma in `Población ETCA (%)`. 352 rows. |
| Variables | Resident population; seasonal ETCA for T1–T4 and the annual total; ETCA population; ETCA as a % of residents |
| Missing values | The Catalonia row has `..` for every ETCA variable (only the resident population is given) |
| Licence | Idescat reuse terms ⚠️ |
| Validation (2026-11-26) | `ETCA = resident + seasonal total` holds for all 43 comarques. Residents sum to 8,012,231, which equals the Catalonia figure. The annual total is not exactly the simple mean of T1–T4 (max difference 383), presumably because quarters are weighted by days. |
| Notes | The resident population here (8,012,231) is a **different population figure** from the 2025 census (8,124,126): it comes from another reference date or source. Do not mix them as denominators. ETCA covers all ages. |

---

## Derived datasets (generated by notebooks, not in Git)

| File in `data/processed/` | Produced by | Content | Known issues |
|---|---|---|---|
| `demographic_municipality_stats_2025.csv` | NB01 | Municipality, total population, 60+ population, % 60+ | Includes the `Catalunya` aggregate as a row |
| `population_by_age_sex_2025.csv` | NB01 | Single-age rows (sex = total) + `age_group` | Includes the `Catalunya` rows. **Note:** despite its name it contains only sex = total. |
| `rfdb_municipality_2023.csv` | NB02 | RFDB per capita 2023 by municipality | Provisional values |
| `seasonal_population_municipality_2024.csv` | NB02 | ETCA for the 22 Costa Brava municipalities + intensity % | Name suggests all municipalities, but it holds only the Costa Brava subset |
| `municipality_analysis_2025.csv` | NB02 | Demographics + RFDB + ETCA, 948 rows | Mixed reference years (2025/2023/2024); includes the Catalunya row |
| `costa_brava_analysis_2025.csv` | NB02 | Costa Brava subset of the above | |

## Candidate sources (not yet downloaded)

Listed to guide the next tasks. None of them have been evaluated yet.

- Idescat census / population estimates **by comarca and age**, historical series (demographic trends by comarca).
- Idescat **population projections** by comarca and age.
- Idescat / INE municipality → comarca code table (to aggregate municipal data and join by code instead of by name).
- INE *Padró continu* and *Estadística continua de població* (cross-checks).
- Generalitat de Catalunya: Departament de Drets Socials, registry of *casals de gent gran* / *Registre d'entitats, serveis i establiments socials (RESES)* (supply side).
- Dades obertes de Catalunya (analisi.transparenciacatalunya.cat): agendas of cultural activities and directories of facilities.
- INE *Encuesta de Condiciones de Vida* and *Encuesta sobre Equipamiento y Uso de TIC en los Hogares* (digital use by age, at Catalonia level).
- Idescat *Enquesta de participació cultural* or equivalent (cultural participation by age).

## Open actions

1. Record the exact URL, download date and SHA-256 of each raw file (see decision D-004 in `decisions_log.md`).
2. Confirm the licence of each specific table.
3. Confirm the reference year of DS-03 from the file header.
4. Get municipal codes for DS-01 and DS-02, so joins use codes instead of names.
