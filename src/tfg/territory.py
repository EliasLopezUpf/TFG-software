"""Territorial reference: municipality -> comarca, at a fixed date.

The analysis uses the comarca division **in force on 1 January 2025**
(42 comarques + Aran), which is the division used by:
  - the 2025 census comarca tables (Idescat censph 539/5976),
  - the base-2024 population projections (Idescat proj),
  - the 2023 RFDB and 2024 ETCA comarca tables.

The Idescat code list (https://www.idescat.cat/codis/?id=50&n=9) gives the
*current* division. Since that date, one municipality has changed comarca:

  - Aiguafreda (080142): Vallès Oriental -> Osona, by Llei 7/2025, of 30 July
    (BOE-A-2025-16832, 14 Aug 2025).

`COMARCA_OVERRIDES_2025_01_01` reverts that change so that municipal data
aggregate exactly to the published 1 Jan 2025 comarca totals (this is checked in
notebook 03). Add any further changes here, with their legal reference.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .paths import IDESCAT_API_RAW

# mun_code -> (comarca_code, comarca_name) in force on 1 January 2025
COMARCA_OVERRIDES_2025_01_01 = {
    "080142": ("41", "Vallès Oriental"),  # Aiguafreda; moved to Osona by Llei 7/2025
}


def load_municipality_codes(path: Path | None = None) -> pd.DataFrame:
    """Idescat municipality code list (current division), unmodified."""
    path = path or IDESCAT_API_RAW / "codis_municipis_comarques.csv"
    codes = pd.read_csv(path, sep=";", skiprows=3, encoding="utf-8-sig", dtype=str)
    codes = codes.loc[:, ["Codi", "Nom", "Codi comarca", "Nom comarca"]]
    codes.columns = ["mun_code", "mun_name", "comarca_code", "comarca_name"]
    return codes


def municipality_to_comarca_2025(path: Path | None = None) -> pd.DataFrame:
    """Municipality -> comarca mapping for the division in force on 1 Jan 2025."""
    mapping = load_municipality_codes(path)
    mapping["comarca_code_current"] = mapping["comarca_code"]
    mapping["comarca_name_current"] = mapping["comarca_name"]
    for mun_code, (com_code, com_name) in COMARCA_OVERRIDES_2025_01_01.items():
        row = mapping["mun_code"] == mun_code
        if row.sum() != 1:
            raise ValueError(f"Override municipality {mun_code} not found exactly once")
        mapping.loc[row, ["comarca_code", "comarca_name"]] = [com_code, com_name]
    mapping["override_applied"] = mapping["comarca_code"] != mapping["comarca_code_current"]
    assert mapping["mun_code"].is_unique
    return mapping
