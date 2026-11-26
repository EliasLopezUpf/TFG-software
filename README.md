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
| `notebooks/03_comarca_demographics.ipynb` | **Comarca level:** 60+/65+/75+ size and share (2025), concentration, threshold sensitivity, constant-boundary trends 2011/2021–2025, Idescat projections to 2049, income and seasonal context | Validated; runs top to bottom |
| `notebooks/04_comarca_profiles_fieldwork.ipynb` | Context by comarca (75+ living alone, urbanisation, IST, education), digital use by age (Catalonia), five rule-based territorial profiles, proposed fieldwork comarques with municipal structure | Validated; runs top to bottom (needs notebook 03 outputs) |
| `notebooks/05_supply_online_visibility_baix_emporda.ipynb` | **Supply, exploratory:** how much of the activity offer for seniors is visible online in Baix Empordà (open cultural agenda, facility and social-services registers, 36 municipal websites) | Validated; runs top to bottom (needs notebook 04 outputs) |

Next steps: agree fieldwork comarques with the tutor, design the supply inventory and the survey (see [`docs/market_study_progress.md`](docs/market_study_progress.md)).

## Repository structure

```
.
├── CLAUDE.md                     # Instructions for the AI agent
├── README.md
├── requirements.txt              # pip freeze (Windows); see "Setup"
├── data/
│   ├── raw/                      # Original files, unmodified, VERSIONED (decision D-004)
│   │   ├── comarca/              # Idescat comarca files downloaded manually by the author
│   │   ├── idescat_api/          # Idescat API downloads + MANIFEST.csv (URL, time, SHA-256)
│   │   ├── opendata_gencat/      # Generalitat open data downloads + MANIFEST.csv
│   │   └── web_checks/           # Observations from municipal website checks
│   └── processed/                # Tables exported by the notebooks (versioned, regenerable)
├── docs/                         # Project documentation (see below)
├── notebooks/
│   ├── 01_demographic_analysis.ipynb      # exploratory, municipal (kept as-is)
│   ├── 02_socioeconomic_analysis.ipynb    # exploratory, municipal (kept as-is)
│   ├── 03_comarca_demographics.ipynb      # comarca-level senior population
│   ├── 04_comarca_profiles_fieldwork.ipynb  # context, profiles, fieldwork candidates
│   └── 05_supply_online_visibility_baix_emporda.ipynb  # supply: online visibility (exploratory)
├── scripts/
│   ├── download_idescat.py       # Reproducible download of the Idescat API tables
│   ├── download_open_data.py     # Generalitat open data (agenda, facilities, social services, town halls)
│   └── check_municipal_websites.py  # Minimal automated check of municipal websites
├── src/tfg/                      # Reusable code
│   ├── idescat.py                # JSON-stat reader, HTML-table reader, age-group helpers
│   ├── paths.py                  # Project paths
│   └── territory.py              # Municipality → comarca mapping (division of 1 Jan 2025)
└── reports/figures/              # Figures exported by the notebooks (versioned, regenerable)
```

Possible later additions, created only when needed: `data/external/` (small reference tables), `data/interim/`, `reports/tables/`.

## Setup

The original environment is Windows with a `.venv` (kernel metadata: Python 3.13.3).

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

`requirements.txt` includes `pywinpty`, which installs only on Windows. On Linux or macOS, remove that line, or install just the packages the notebooks need:

```bash
pip install pandas==3.1.0 numpy==2.5.4 matplotlib==3.11.2 jupyter
```

## Data

The raw data is in the repository (`data/raw/`), so notebooks 03+ run directly after cloning. To re-download the Idescat API tables (this updates `data/raw/idescat_api/MANIFEST.csv`):

```bash
python scripts/download_idescat.py --force
```

Notebooks 01–02 use municipal files that are not in the repository; see [`docs/data_sources.md`](docs/data_sources.md) (DS-01 to DS-03).

Run the notebooks in numerical order. Notebook 03 is independent of 01–02.

Source: **Idescat** (Institut d'Estadística de Catalunya). Reuse is subject to Idescat's terms: attribution is required, and data must not be altered when presented. See [`docs/data_sources.md`](docs/data_sources.md).

## Documentation

| File | Purpose |
|---|---|
| [`docs/project_summary.md`](docs/project_summary.md) | Concept, scope, roadmap, current state |
| [`docs/research_log.md`](docs/research_log.md) | Chronological research record |
| [`docs/decisions_log.md`](docs/decisions_log.md) | Methodological decisions and open questions |
| [`docs/data_sources.md`](docs/data_sources.md) | Dataset registry: source, period, granularity, licence |
| [`docs/market_study_progress.md`](docs/market_study_progress.md) | Work-package tracker |
| [`docs/existing_work_review.md`](docs/existing_work_review.md) | Audit of notebooks 01–02 |
| [`docs/notebook_03_summary.md`](docs/notebook_03_summary.md) | Plain-language summary of notebook 03 (results, method, limitations) |
