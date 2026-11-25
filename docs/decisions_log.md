# Decisions Log

Methodological and project decisions. Status: **Adopted** · **Proposed** (awaiting the author's or tutor's approval) · **Superseded**.

| ID | Date | Decision | Rationale | Status |
|---|---|---|---|---|
| D-001 | 2026-11 | Geographic scope = Catalonia, primary unit = comarca. The Costa Brava is an exploratory case only. | Tutor guidance; the market should not be bounded by the initial observation. | Adopted (to confirm with the tutor) |
| D-002 | 2026-10 | Working target population = 60+. Also explore 65+ and 75+. | Provisional analytical definition; not a commercial segment. | Adopted (provisional) |
| D-003 | 2026-10 | Use the Idescat **census** (`censph`) as the population source rather than the Padró. | Idescat designates the census and estimates as its reference population figures. | Adopted (implicitly, in notebook 01). Now documented. |
| D-004 | 2026-11-25 | Raw data policy: keep `data/raw/` out of Git, but commit a **manifest** (`data/raw/MANIFEST.md` or a section in `data_sources.md`) with the URL, download date and SHA-256 of each file, plus download instructions or scripts. Alternative: commit the small raw CSVs (Idescat CC BY-style terms appear to allow redistribution with attribution). | Reproducibility versus repository size and licence clarity. | **Proposed**: the author must choose |
| D-005 | 2026-11-25 | Do **not** edit notebooks 01 and 02 in place. Correct the known issues (Catalunya row, mixed years, opportunity score) in the new comarca-level notebooks, and mark 01 and 02 as "exploratory, superseded" in the README. | Preserves the historical work; avoids silently changing earlier results. | **Proposed** |
| D-006 | 2026-11-25 | Adopt the repository structure described in `README.md` ("Proposed structure"). Create folders only when the first file needs them. | Supports provenance, reusable code and reports without reorganising existing work. | **Proposed** |
| D-007 | 2026-11-25 | Do not use composite "opportunity scores" with arbitrary weights. Any prioritisation must use transparent indicators and include a sensitivity analysis of the weights. | The handover explicitly recommends against arbitrary composite scores; rankings were sensitive to weights and to sample-relative MinMax scaling. | **Proposed** |
| D-008 | 2026-11-25 | Join territorial datasets by **official municipal code** (INE/Idescat, 6 digits) rather than by name, using an official municipality→comarca table. | Name joins are fragile (articles, renamings, mergers). | **Proposed** |
| D-009 | 2026-11-25 | Always exclude aggregate rows (`Catalunya`, provinces, comarques) before aggregating municipal data, and assert the result reconciles with the official aggregate. | Prevents the double counting found in notebook 01. | **Proposed** |
| D-010 | 2026-11-25 | Use the `CLAUDE.md` documentation files in `docs/` (not the repository root). | Keeps the root clean; `CLAUDE.md` updated accordingly. | Adopted |

## Unresolved questions

- Which target threshold(s) should be the final one(s): 60+, 65+, 75+? (tutor)
- Expected deliverable: a complete business plan or a feasibility study? Is a prototype required? (tutor)
- Survey scale, recruitment method and ethics approval process at UPF.
- Whether to commit raw data (D-004).
