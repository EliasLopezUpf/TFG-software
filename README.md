# TFG — Senior Activity Marketplace

Data Science Bachelor's Thesis (UPF). This is a data-driven feasibility study and business plan for a digital marketplace that connects senior citizens with activities, events and experiences offered by municipalities, associations, *casals de gent gran*, community centres, cultural and sports organisations, and private organisers.

- **Scope:** Catalonia, with **comarques** as the primary unit of analysis. The Costa Brava was the initial exploratory case.
- **Working population:** 60+ (provisional; 65+ and 75+ also explored).
- Full context: [`docs/project_summary.md`](docs/project_summary.md) · agent instructions: [`CLAUDE.md`](CLAUDE.md)

## Current status

| Notebook | Content | Status |
|---|---|---|
| `notebooks/01_demographic_analysis.ipynb` | 2025 population by age and municipality (Idescat census); 60+ share; Costa Brava sample | Exploratory. Known issues, see [review](docs/existing_work_review.md) |
| `notebooks/02_socioeconomic_analysis.ipynb` | RFDB 2023, ETCA seasonal population 2024; Costa Brava case | Exploratory. Known issues, see [review](docs/existing_work_review.md) |

Next step: demographic market sizing **by comarca** (see [`docs/market_study_progress.md`](docs/market_study_progress.md)).

## Repository structure

Current:

```
.
├── CLAUDE.md                 # Instructions for the AI agent
├── README.md
├── requirements.txt          # pip freeze (Windows); see "Setup"
├── data/
│   ├── raw/                  # Original downloads (gitignored, never modified)
│   └── processed/            # Notebook outputs (gitignored)
├── docs/
│   ├── project_summary.md
│   ├── research_log.md
│   ├── decisions_log.md
│   ├── data_sources.md       # Dataset registry and provenance
│   ├── market_study_progress.md
│   ├── existing_work_review.md
│   └── TFG_Project_Summary_Claude_Code_Handover.docx
├── notebooks/
│   ├── 01_demographic_analysis.ipynb
│   └── 02_socioeconomic_analysis.ipynb
└── reports/                  # Generated outputs (gitignored)
```

Proposed additions (decision D-006, *pending approval*; folders are created only when first needed, and nothing existing is moved):

```
data/
├── raw/<source>/             # One subfolder per source (e.g. idescat_censph/)
├── external/                 # Small official reference tables (e.g. municipality→comarca codes), committed
├── interim/                  # Intermediate cleaned tables (gitignored)
└── processed/                # Analysis-ready tables (gitignored)
notebooks/
├── 01_…, 02_…                # Kept as-is (exploratory, superseded later)
├── 03_comarca_demographics.ipynb
└── …                         # NN_short_topic.ipynb, numbered in execution order
src/tfg/                      # Reusable Python code (paths, loaders, harmonisation, validation)
scripts/                      # Data download scripts (record URL, date, checksum)
reports/
├── figures/
└── tables/
```

## Setup

The original environment is Windows with a `.venv` (kernel metadata: Python 3.13.3).

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

`requirements.txt` includes `pywinpty`, which installs only on Windows. On Linux or macOS, remove that line before installing.

## Data

No data is stored in Git (`data/raw/` and `data/processed/` are gitignored). To run the notebooks, download the raw files listed in [`docs/data_sources.md`](docs/data_sources.md) into `data/raw/` using the exact filenames given there, then run the notebooks in numerical order (notebook 02 reads notebook 01's output).

Sources: Idescat (Institut d'Estadística de Catalunya). Reuse is subject to Idescat's terms (attribution required).

## Documentation

| File | Purpose |
|---|---|
| [`docs/project_summary.md`](docs/project_summary.md) | Concept, scope, roadmap, current state |
| [`docs/research_log.md`](docs/research_log.md) | Chronological research record |
| [`docs/decisions_log.md`](docs/decisions_log.md) | Methodological decisions and open questions |
| [`docs/data_sources.md`](docs/data_sources.md) | Dataset registry: source, period, granularity, licence |
| [`docs/market_study_progress.md`](docs/market_study_progress.md) | Work-package tracker |
| [`docs/existing_work_review.md`](docs/existing_work_review.md) | Audit of notebooks 01–02 |
