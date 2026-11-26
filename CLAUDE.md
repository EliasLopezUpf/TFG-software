
# TFG - Senior Activity Marketplace

## 1. Project Overview

This repository contains the research and data analysis for a Data Science Bachelor's Thesis (TFG).

The project investigates the feasibility of a marketplace that connects senior citizens with activities, experiences and events offered by municipalities, associations, community centers and private organizers.

The objective is to use data science, demographic analysis, market research and empirical research to assess the business opportunity and develop a data-driven business plan.

The Costa Brava was the initial exploratory area, but the project is not geographically limited to the Costa Brava.

The current geographical scope of the market study is Catalonia, with comarca-level analysis as the primary territorial unit.

## 2. Main Research Objective

Assess whether there is a viable business opportunity for a digital marketplace connecting the senior population with activities and experiences adapted to their interests and needs.

## 3. Research Priorities

- Quantify and characterize the senior population.
- Study demographic trends and growth.
- Identify potentially relevant comarques.
- Analyze socioeconomic and territorial characteristics.
- Investigate the existing activity supply.
- Research user needs through surveys and interviews.
- Assess the marketplace value proposition.
- Develop and evaluate potential business models.
- Estimate business feasibility.

## 4. Working Population Definition

The initial target population is people aged 60 and older (60+).

This is a provisional analytical definition, not a final commercial segmentation.

Explore alternative thresholds such as 65+ and 75+ when relevant.

Never assume all people aged 60+ are potential customers.

## 5. Geographic Scope

Catalonia is the initial region of exploration.

Comarques are the primary unit of analysis for market sizing and territorial comparison.

Municipal-level data may be used for:
- Detailed territorial analysis.
- Activity supply mapping.
- Survey design.
- Validation of comarca-level results.

The Costa Brava is an initial case study, not the definitive market boundary.

## 6. Preferred Tools

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn only when justified
- Jupyter Notebook
- Git and GitHub

Use the existing project environment and tools whenever possible.

Do not introduce additional technologies without explaining why they are useful.

## 7. Data Research Rules

- Prioritize official and reliable sources.
- Prefer Idescat, INE, Generalitat de Catalunya, public administrations and other authoritative sources.
- Search for datasets before assuming they do not exist.
- Document every dataset.
- Preserve raw data.
- Do not silently modify raw data.
- Document cleaning, transformations and exclusions.
- Record dataset publication date, reference period, geographical granularity and source.
- Check licenses and redistribution restrictions.
- Never fabricate data, sources, statistics or citations.
- Clearly distinguish measured data, assumptions and estimates.

## 8. Analysis Rules

- Create reproducible notebooks.
- Explain the purpose of each analysis.
- Use clear and descriptive variable names.
- Validate transformations.
- Check missing values, duplicates and inconsistencies.
- Document methodological limitations.
- Avoid unnecessary machine learning.
- Use analytical methods only when they answer a relevant research question.
- Do not make causal claims from descriptive analysis.

## 9. Notebook Structure

Each notebook should contain:

1. Objective and research questions.
2. Data sources.
3. Data preparation.
4. Exploratory analysis.
5. Analytical methods.
6. Results and visualizations.
7. Interpretation.
8. Limitations.
9. Conclusions and next steps.

## 10. Market Research

Investigate both sides of the marketplace:

### Demand
- Senior citizens.
- Activity preferences.
- Participation patterns.
- Barriers.
- Information discovery.
- Digital preferences.
- Accessibility.

### Supply
- Municipalities.
- Associations.
- Casals de gent gran.
- Community and civic centers.
- Cultural organizations.
- Sports and social clubs.
- Private organizers.

Do not assume that lack of online information means lack of activities.

## 11. Documentation

Maintain the following documents (all in `docs/`):

- docs/project_summary.md
- docs/research_log.md
- docs/decisions_log.md
- docs/data_sources.md
- docs/market_study_progress.md
- docs/existing_work_review.md (audit of notebooks 01–02; extend when reviewing earlier work)

Update relevant documents after completing significant work.

Record important methodological decisions and unresolved questions.

## 12. Agent Workflow

Before starting a new task:

1. Inspect the existing repository.
2. Read CLAUDE.md and project documentation.
3. Check existing notebooks and datasets.
4. Avoid duplicating work.
5. Propose a plan for substantial tasks.

For substantial research tasks:

- Search for datasets and sources.
- Explain the proposed methodology.
- Implement the analysis.
- Execute and validate code.
- Generate outputs.
- Document conclusions and limitations.
- Update the research log.

Do not silently overwrite existing files.

## 13. Autonomy

You may independently:

- Search for datasets.
- Download public data when permitted.
- Create new notebooks.
- Write reusable Python code.
- Generate charts and tables.
- Create documentation.
- Perform exploratory analyses.
- Run code and validate outputs.

Before:

- Deleting existing data or files.
- Overwriting important existing work.
- Changing the project scope.
- Making major methodological decisions.
- Installing substantial new dependencies.
- Publishing data or personal information.
- Committing or pushing changes.

Explain the action and obtain approval when appropriate.

## 14. Research Integrity

The goal is to produce a rigorous, reproducible and honest TFG.

Do not manufacture conclusions to support the marketplace idea.

If the data does not support the initial hypothesis, report it.

Clearly separate:

- Facts.
- Observations.
- Hypotheses.
- Assumptions.
- Recommendations.

The business model must emerge from the research, rather than being predetermined.

## 15. Repository State and Conventions

*Added 2026-11-25 after the initial repository audit. Keep this section current.*

### Current layout
- `notebooks/01_…`, `02_…`: exploratory, municipal level. **Do not edit in place** (D-005). Their known issues are fixed in later notebooks.
- `notebooks/03_comarca_demographics.ipynb`: comarca-level senior population (size, share, trends at constant boundaries, projections, context). Its exported tables in `data/processed/comarca_*.csv` are the starting point for later comarca work.
- `data/raw/` is **versioned** (D-004). `data/raw/idescat_api/` is produced by `scripts/download_idescat.py`, with `MANIFEST.csv`. `data/raw/comarca/` holds files the author downloaded manually. `data/processed/` and `reports/` are also versioned (2026-11-26); re-run the producing notebook before committing so outputs match the code.
- Reusable code lives in `src/tfg/` (`idescat.read_jsonstat`, `territory.municipality_to_comarca_2025`, `paths`). Notebooks import it via `sys.path.insert(0, PROJECT_ROOT / "src")`.
- A local `.venv` (gitignored) with the pinned versions from `requirements.txt` is used to execute notebooks: `jupyter nbconvert --to notebook --execute --inplace`.

### Known pitfalls in the data (see `docs/existing_work_review.md`)
- Idescat municipal exports include an aggregate `Catalunya` row. **Always remove aggregate rows** before summing municipalities, and assert the result reconciles with the official total.
- Join territorial data by **6-digit municipal code**, not by name, wherever codes are available.
- Comarca boundaries change over time (Moianès 2015; Lluçanès and Biosca/Torà 2023; Aiguafreda → Osona by Llei 7/2025). Use the **1 Jan 2025 division** (`src/tfg/territory.py`, D-011), and build time series from municipal data at constant boundaries (D-012).
- The Idescat API returns at most 20,000 values per request. Split requests (see `scripts/download_idescat.py`) and do not re-request data you already have (API terms).
- Reference years differ across sources (census 2025, RFDB 2023 provisional, ETCA 2024). State the year of every indicator.
- RFDB and ETCA only cover municipalities with ≥1,000 inhabitants. Prefer Idescat's comarca-level tables over aggregating incomplete municipal data.
- RFDB is all-household income (not senior income). ETCA is all-age population load (not senior tourism).
- Census population (`censph`) ≠ Padró. Do not mix them without saying so.
- Do not reuse the "opportunity score" from notebook 02 (arbitrary weights).

### Conventions
- Notebooks: `notebooks/NN_short_topic.ipynb`, numbered in execution order. Follow the §9 structure. They must run top to bottom (Restart & Run All) before committing.
- Paths: derive from a project root (`PROJECT_ROOT`); never hard-code absolute or user-specific paths.
- Each new raw dataset: add an entry to `docs/data_sources.md` (URL, download date, reference period, granularity, licence, checksum) **before** using it.
- Variable names in English and descriptive. Original source column names may be kept in raw-data loading code.
- Environment: the author works on Windows (Python 3.13 venv per the kernel metadata). `requirements.txt` contains `pywinpty` (Windows-only); remove it to install on Linux or macOS.
