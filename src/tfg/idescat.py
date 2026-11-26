"""Helpers for Idescat data.

- `read_jsonstat`: convert a JSON-stat 2.0 dataset (as returned by the Idescat
  Tables API v2, https://api.idescat.cat/taules/v2) into a tidy pandas DataFrame.
- Age-group helpers for Idescat five-year age labels.

Only the standard library, NumPy and pandas are used.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def _category_ids(dimension: dict) -> list[str]:
    index = dimension["category"]["index"]
    if isinstance(index, list):
        return list(index)
    # dict form: {id: position}
    return [k for k, _ in sorted(index.items(), key=lambda kv: kv[1])]


def read_jsonstat(path_or_dict, label_columns: bool = True) -> pd.DataFrame:
    """Return a tidy DataFrame with one row per cell of a JSON-stat dataset.

    For every dimension `D` the output has a column `D` (category id) and, if
    `label_columns`, a column `D_label` (category label). Values go in `value`,
    and the Idescat status flag (e.g. 'p' provisional, '..' not available)
    goes in `status`. Missing cells are NaN.
    """
    if isinstance(path_or_dict, (str, Path)):
        with open(path_or_dict, encoding="utf-8") as fh:
            ds = json.load(fh)
    else:
        ds = path_or_dict
    if ds.get("class") != "dataset":
        raise ValueError(f"Not a JSON-stat dataset: class={ds.get('class')!r}")

    dim_ids = ds["id"]
    sizes = ds["size"]
    n_cells = int(np.prod(sizes))

    # Values may be a dense list or a sparse {position: value} dict
    raw_values = ds["value"]
    values = np.full(n_cells, np.nan)
    if isinstance(raw_values, dict):
        for pos, v in raw_values.items():
            values[int(pos)] = np.nan if v is None else v
    else:
        values[:] = [np.nan if v is None else v for v in raw_values]

    status = np.full(n_cells, None, dtype=object)
    raw_status = ds.get("status")
    if isinstance(raw_status, dict):
        for pos, s in raw_status.items():
            status[int(pos)] = s
    elif isinstance(raw_status, list):
        status[:] = raw_status
    elif isinstance(raw_status, str):
        status[:] = raw_status

    # Row-major cartesian product of category ids (JSON-stat ordering)
    ids_per_dim = [_category_ids(ds["dimension"][d]) for d in dim_ids]
    grids = np.meshgrid(*[np.arange(s) for s in sizes], indexing="ij")
    frame = {}
    for d, ids, grid in zip(dim_ids, ids_per_dim, grids):
        ids_arr = np.array(ids, dtype=object)
        frame[d] = ids_arr[grid.ravel()]
        if label_columns:
            labels = ds["dimension"][d]["category"].get("label", {})
            frame[f"{d}_label"] = np.array(
                [labels.get(i, i) for i in ids], dtype=object
            )[grid.ravel()]
    frame["value"] = values
    frame["status"] = status
    return pd.DataFrame(frame)


# --- Five-year age groups -------------------------------------------------

def age_group_lower_bound(label: str) -> float:
    """Lower bound of an Idescat five-year age label.

    'de 60 a 64 anys' -> 60, '100 anys o més' -> 100, 'total' -> NaN.
    Also accepts API ids such as 'Y060_064' or 'Y_GE100'.
    """
    label = str(label).strip()
    if label.lower() in {"total", "totals"}:
        return np.nan
    if label.startswith("Y"):
        digits = "".join(ch if ch.isdigit() else " " for ch in label).split()
        return float(digits[0]) if digits else np.nan
    digits = "".join(ch if ch.isdigit() else " " for ch in label).split()
    return float(digits[0]) if digits else np.nan


# --- Idescat "f=xls" table exports (HTML tables) ------------------------------

def _to_number(text: str) -> float:
    """'3.061.495' -> 3061495.0 ; '99,3' -> 99.3 ; '..' / '' -> NaN."""
    text = text.strip().replace("\xa0", "")
    if text in {"", "..", "...", "-", "—"}:
        return np.nan
    return float(text.replace(".", "").replace(",", "."))


def read_idescat_html_tables(path) -> list[tuple[str, pd.DataFrame]]:
    """Parse an Idescat table export (an HTML file served with an .xls name).

    Returns a list of (caption, DataFrame). Each DataFrame has one row per data
    row, with `group` (the section heading row above it, e.g. 'Edat'),
    `category` (the row label) and one numeric column per header cell.
    Only the standard library, NumPy and pandas are used.
    """
    import html
    import re

    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    clean = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
    tables = []
    for table in re.findall(r"<table.*?</table>", raw, flags=re.S):
        caption = re.search(r"<caption[^>]*>(.*?)</caption>", table, flags=re.S)
        caption = clean(caption.group(1)) if caption else ""
        body = re.search(r"<tbody[^>]*>(.*?)</tbody>", table, flags=re.S)
        head = re.search(r"<thead[^>]*>(.*?)</thead>", table, flags=re.S)
        header_rows = re.findall(r"<tr.*?</tr>", head.group(1) if head else table, flags=re.S)
        header = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", header_rows[0], flags=re.S)]
        columns = header[1:]
        records, group = [], None
        for row in re.findall(r"<tr.*?</tr>", body.group(1) if body else table, flags=re.S):
            cells = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, flags=re.S)]
            if not cells or cells == header:
                continue
            if len(cells) == 1 or all(c == "" for c in cells[1:]):
                group = cells[0]
                continue
            if len(cells) != len(columns) + 1:
                continue
            records.append({"group": group, "category": cells[0],
                            **{col: _to_number(v) for col, v in zip(columns, cells[1:])}})
        tables.append((caption, pd.DataFrame(records)))
    return tables
