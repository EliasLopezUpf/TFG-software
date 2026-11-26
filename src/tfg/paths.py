"""Project paths, derived from the repository root (no hard-coded user paths)."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_EXTERNAL = PROJECT_ROOT / "data" / "external"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_FIGURES = PROJECT_ROOT / "reports" / "figures"
REPORTS_TABLES = PROJECT_ROOT / "reports" / "tables"

IDESCAT_API_RAW = DATA_RAW / "idescat_api"
COMARCA_RAW = DATA_RAW / "comarca"
