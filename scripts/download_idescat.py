"""Download the Idescat tables used by the comarca-level analysis.

Usage (from the repository root):

    python scripts/download_idescat.py            # download missing files only
    python scripts/download_idescat.py --force    # re-download everything

Every file is saved unmodified in data/raw/idescat_api/ (JSON-stat 2.0 from the
Idescat Tables API v2, or the original CSV for the territorial code list).
Each download is recorded in data/raw/idescat_api/MANIFEST.csv with the URL,
UTC retrieval time, SHA-256 and the table's own "updated" date, if it has one.

Idescat API terms of use (https://www.idescat.cat/dev/api/#cdu): credit
Idescat as the source, do not alter the data when presenting it, and avoid
repeating the same request within a short time. This script therefore skips
files that already exist and pauses between requests.

The API returns at most 20,000 values per request, so the larger tables are
split into several requests (one file each).
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
OUT_DIR = ROOT / "data" / "raw" / "idescat_api"
MANIFEST = OUT_DIR / "MANIFEST.csv"
API = "https://api.idescat.cat/taules/v2"
PAUSE_SECONDS = 1.0

AGE_IDS_PART_A = [
    "Y000_004", "Y005_009", "Y010_014", "Y015_019", "Y020_024", "Y025_029",
    "Y030_034", "Y035_039", "Y040_044", "Y045_049", "Y050_054",
]
ESTIMATE_YEARS = range(2012, 2026)          # population on 1 January (S1)
CENSUS_YEARS = [2011, 2021, 2022, 2023, 2024, 2025]
PROJECTION_YEARS_A = range(2024, 2037)      # base 2024 projections, split in two
PROJECTION_YEARS_B = range(2037, 2050)
PROJECTION_TABLES = {                      # scenario -> (node, table)
    "low": ("20953", "24798"),
    "medium": ("20957", "24801"),
    "high": ("20961", "24804"),
}


def build_requests(age_ids_part_b: list[str]) -> list[dict]:
    """List every request as {name, url, description}."""
    reqs = []

    # 1. Census 2011, 2021-2025, comarques (boundaries in force each year)
    reqs.append(dict(
        name="censph_539_5976_com.json",
        url=f"{API}/censph/539/5976/com/data?lang=ca",
        description="Census: population by sex and five-year age, comarques, 2011 and 2021-2025",
    ))

    # 2. Population estimates on 1 January, comarques, sex = total
    years = ",".join(f"{y}S1" for y in ESTIMATE_YEARS)
    reqs.append(dict(
        name="ep_9124_20150_com_S1_total.json",
        url=f"{API}/ep/9124/20150/com/data?SEMESTER={years}&SEX=TOTAL&lang=ca",
        description="Population estimates by five-year age, comarques, 1 Jan 2012-2025, sex total",
    ))

    # 3. Census, municipalities, sex = total, 2011 and 2021-2025.
    #    Used to rebuild comarques with constant (current) boundaries.
    #    One year and half of the age groups per request (API limit).
    for year in CENSUS_YEARS:
        for part, ages in (("a", AGE_IDS_PART_A), ("b", age_ids_part_b)):
            reqs.append(dict(
                name=f"censph_539_5976_mun_{year}_total_{part}.json",
                url=(f"{API}/censph/539/5976/mun/data?YEAR={year}&SEX=TOTAL"
                     f"&AGE={','.join(ages)}&lang=ca"),
                description=f"Census: population by five-year age, municipalities, {year}, sex total, ages part {part}",
            ))

    # 4. Projections (base 2024), comarques, sex = total, three scenarios
    for scen, (node, table) in PROJECTION_TABLES.items():
        for part, yrs in (("a", PROJECTION_YEARS_A), ("b", PROJECTION_YEARS_B)):
            reqs.append(dict(
                name=f"proj_{node}_{table}_com_{scen}_total_{part}.json",
                url=(f"{API}/proj/{node}/{table}/com/data?SEX=TOTAL"
                     f"&YEAR={','.join(str(y) for y in yrs)}&lang=ca"),
                description=f"Projected population on 1 Jan by five-year age, comarques, {scen} scenario (base 2024), {yrs.start}-{yrs.stop - 1}, sex total",
            ))

    # 5. Municipality -> comarca code list (current territorial division)
    reqs.append(dict(
        name="codis_municipis_comarques.csv",
        url="https://www.idescat.cat/codis/?id=50&n=9&f=ssv",
        description="Idescat territorial codes: municipalities with their comarca (current division)",
    ))

    # --- Context variables (notebook 04) ------------------------------------
    # 6. Census household indicators, 2021 (incl. % of people 75+ living alone).
    #    Municipal level is used to rebuild the 1 Jan 2025 comarques; the
    #    comarca table (2021 boundaries) is kept for validation.
    for geo in ("mun", "com"):
        reqs.append(dict(
            name=f"censph_17317_20806_{geo}.json",
            url=f"{API}/censph/17317/20806/{geo}/data?lang=ca",
            description=f"Census household indicators, 2021, {'municipalities' if geo == 'mun' else 'comarques (2021 boundaries)'}",
        ))
    # 7. Census education indicators (population 15+), 2021-2024, comarques
    reqs.append(dict(
        name="censph_16719_20207_com.json",
        url=f"{API}/censph/16719/20207/com/data?lang=ca",
        description="Census education indicators (population aged 15+), comarques, 2021-2024 (boundaries in force each year)",
    ))
    # 8. Degree of urbanisation indicators (population, area, density, % in
    #    urban centres / towns / rural cells), 2025: municipalities + comarques
    reqs.append(dict(
        name="degurba_17107_20579_mun_2025.json",
        url=f"{API}/degurba/17107/20579/mun/data?YEAR=2025&lang=ca",
        description="Degree of urbanisation indicators, municipalities, 2025",
    ))
    reqs.append(dict(
        name="degurba_17107_20579_com.json",
        url=f"{API}/degurba/17107/20579/com/data?lang=ca",
        description="Degree of urbanisation indicators, comarques, 2025",
    ))
    # 9. Territorial socioeconomic index (IST) and its component values, comarques
    reqs.append(dict(
        name="ist_14034_14994_com.json",
        url=f"{API}/ist/14034/14994/com/data?lang=ca",
        description="Territorial socioeconomic index (IST, Catalonia = 100), comarques, 2015-2024",
    ))
    reqs.append(dict(
        name="ist_14074_15022_com.json",
        url=f"{API}/ist/14074/15022/com/data?lang=ca",
        description="Socioeconomic indicators (IST components, values), comarques, 2015-2024",
    ))
    # 10. ICT use by age, Catalonia, 2025 (Idescat/INE household ICT survey).
    #     Not in the API: Idescat's table export (an HTML table served as .xls).
    reqs.append(dict(
        name="ticll25_1_2_1_ict_use_by_person.html",
        url="https://www.idescat.cat/pub/?id=ticll25&n=1.2.1&f=xls",
        description="ICT household survey 2025: main ICT use indicators by demographic characteristics (persons 16-74), Catalonia",
    ))
    return reqs


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "tfg-research-script"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def age_ids_part_b() -> list[str]:
    """Read the remaining age ids from the table metadata (no guessing)."""
    meta = json.loads(fetch(f"{API}/censph/539/5976/mun?lang=ca"))
    index = meta["dimension"]["AGE"]["category"]["index"]
    ids = list(index) if isinstance(index, list) else sorted(index, key=index.get)
    rest = [i for i in ids if i not in AGE_IDS_PART_A]
    assert len(ids) == 22 and len(rest) == 11, ids
    return rest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = {}
    if MANIFEST.exists():
        with open(MANIFEST, newline="", encoding="utf-8") as fh:
            manifest_rows = {r["file"]: r for r in csv.DictReader(fh)}

    requests_ = build_requests(age_ids_part_b())
    for r in requests_:
        target = OUT_DIR / r["name"]
        if target.exists() and not args.force:
            continue
        content = fetch(r["url"])
        if r["name"].endswith(".json"):
            payload = json.loads(content)
            if payload.get("class") == "error":
                print(f"API error for {r['name']}: {payload}", file=sys.stderr)
                return 1
            updated = payload.get("updated", "")
        else:
            updated = ""
        target.write_bytes(content)
        manifest_rows[r["name"]] = dict(
            file=r["name"],
            url=r["url"],
            description=r["description"],
            retrieved_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            sha256=hashlib.sha256(content).hexdigest(),
            bytes=len(content),
            table_updated=updated,
        )
        print(f"downloaded {r['name']} ({len(content):,} bytes)")
        time.sleep(PAUSE_SECONDS)

    fields = ["file", "url", "description", "retrieved_utc", "sha256", "bytes", "table_updated"]
    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for name in sorted(manifest_rows):
            writer.writerow(manifest_rows[name])
    print(f"{len(requests_)} files listed; manifest: {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
