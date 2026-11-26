"""Download Generalitat de Catalunya open data used by notebook 05 (activity supply).

Usage (from the repository root):

    python scripts/download_open_data.py            # download missing files only
    python scripts/download_open_data.py --force    # re-download everything

Source: Dades obertes de Catalunya (https://analisi.transparenciacatalunya.cat),
Socrata API. Files are saved unmodified (JSON) in data/raw/opendata_gencat/ and
recorded in data/raw/opendata_gencat/MANIFEST.csv (URL, UTC time, SHA-256,
dataset "rows updated" time).

Only the columns needed for the analysis are requested. Personal data present in
some datasets (e.g. names of mayors, contact persons, NIF) are deliberately NOT
downloaded.

Scope: comarca of Baix Empordà (exploratory supply case), plus one aggregated
Catalonia-wide count used for context.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw" / "opendata_gencat"
MANIFEST = OUT_DIR / "MANIFEST.csv"
BASE = "https://analisi.transparenciacatalunya.cat"
PAUSE_SECONDS = 1.0

REQUESTS = [
    dict(
        name="agenda_cultural_baix_emporda.json",
        dataset="rhpv-yr4f",
        description="Agenda cultural de Catalunya (per localitzacions): all events located in Baix Empordà",
        params={
            "$select": "codi, denominaci, subt_tol, data_inici, data_fi, data_fi_aproximada, tags_mbits, "
                       "tags_categor_es, tags_altres_categor_es, gratuita, entrades, modalitat, espai, "
                       "comarca_i_municipi, comarca, municipi, descripcio, urlactivitat, data_creacio",
            "$where": "comarca like 'agenda:ubicacions/girona/baix-emporda%'",
            "$order": "codi",
            "$limit": "50000",
        },
    ),
    dict(
        name="equipaments_baix_emporda.json",
        dataset="8gmd-gz7i",
        description="Equipaments de Catalunya: all public facilities registered in Baix Empordà",
        params={
            "$select": "idequipament, nom, categoria, poblacio, codi_municipi, comarca, web, data_modificacio",
            "$where": "upper(comarca) in ('BAIX EMPORDÀ', 'BAIX EMPORDA')",
            "$order": "idequipament",
            "$limit": "50000",
        },
    ),
    dict(
        name="equipaments_casals_gent_gran_by_comarca.json",
        dataset="8gmd-gz7i",
        description="Equipaments de Catalunya: number of facilities in the category 'Casals de gent gran', by comarca (all Catalonia)",
        params={
            "$select": "comarca, count(*) AS n",
            "$where": "categoria like '%Casals de gent gran%'",
            "$group": "comarca",
            "$order": "n DESC",
            "$limit": "1000",
        },
    ),
    dict(
        name="reses_baix_emporda.json",
        dataset="ivft-vegh",
        description="Registre d'entitats, serveis i establiments socials: services in Baix Empordà",
        params={
            "$select": "registre, nom, tipologia, inscripcio, capacitat, municipi, comarca, qualificacio",
            "$where": "comarca = 'Baix Empordà'",
            "$order": "registre",
            "$limit": "50000",
        },
    ),
    dict(
        name="ajuntaments_baix_emporda.json",
        dataset="vevv-8fvw",
        description="Dades d'ens locals - Ajuntaments: municipal code, name, population and official website (Baix Empordà)",
        params={
            "$select": "codi_municipi, municipi, comarca, cens, any_cens, web",
            "$where": "comarca = 'Baix Empordà'",
            "$order": "municipi",
            "$limit": "1000",
        },
    ),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "tfg-research-script"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    if MANIFEST.exists():
        with open(MANIFEST, newline="", encoding="utf-8") as fh:
            manifest = {r["file"]: r for r in csv.DictReader(fh)}

    for r in REQUESTS:
        target = OUT_DIR / r["name"]
        if target.exists() and not args.force:
            continue
        url = f"{BASE}/resource/{r['dataset']}.json?{urllib.parse.urlencode(r['params'])}"
        content = fetch(url)
        rows = json.loads(content)
        meta = json.loads(fetch(f"{BASE}/api/views/{r['dataset']}.json"))
        rows_updated = meta.get("rowsUpdatedAt")
        rows_updated = (datetime.fromtimestamp(rows_updated, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                        if rows_updated else "")
        target.write_bytes(content)
        manifest[r["name"]] = dict(
            file=r["name"], dataset=r["dataset"], dataset_name=meta.get("name", ""),
            url=url, description=r["description"],
            retrieved_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            dataset_rows_updated_utc=rows_updated, rows=len(rows),
            sha256=hashlib.sha256(content).hexdigest(), bytes=len(content),
            attribution=meta.get("attribution", ""),
        )
        print(f"downloaded {r['name']}: {len(rows):,} rows")
        time.sleep(PAUSE_SECONDS)

    fields = ["file", "dataset", "dataset_name", "url", "description", "retrieved_utc",
              "dataset_rows_updated_utc", "rows", "sha256", "bytes", "attribution"]
    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for name in sorted(manifest):
            w.writerow(manifest[name])
    return 0


if __name__ == "__main__":
    sys.exit(main())
