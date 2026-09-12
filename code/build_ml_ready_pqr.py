"""Combine annual PQR exports and reshape Tableau measures to one row per transaction."""

from __future__ import annotations

import csv
import glob
import json
import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_GLOB = str(ROOT / "global_fund" / "pqr_transactions_by_year" / "pqr_transactions_*.csv")
OUT_DIR = ROOT / "global_fund" / "derived"


def snake_case(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def main() -> None:
    files = sorted(glob.glob(RAW_GLOB))
    if len(files) != 24:
        raise RuntimeError(f"Expected 24 annual extracts (2003–2026), found {len(files)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    long_path = OUT_DIR / "pqr_transactions_2003_2026_long.csv"
    wide_path = OUT_DIR / "pqr_transactions_2003_2026_ml_ready.csv"
    qa_path = ROOT / "documentation" / "pqr_extraction_qa.json"

    transactions: dict[str, dict[str, str]] = {}
    schemas: set[tuple[str, ...]] = set()
    measure_counts: Counter[str] = Counter()
    annual_long_rows: Counter[str] = Counter()
    excluded_summary_rows = 0
    excluded_invalid_rows = 0
    long_rows = 0

    long_writer = None
    with long_path.open("w", encoding="utf-8", newline="") as long_handle:
        for file_path in files:
            extract_year = Path(file_path).stem.rsplit("_", 1)[-1]
            with open(file_path, encoding="utf-8-sig", newline="") as source:
                reader = csv.DictReader(source)
                if not reader.fieldnames:
                    raise RuntimeError(f"Missing header: {file_path}")
                schemas.add(tuple(reader.fieldnames))
                if long_writer is None:
                    long_fields = [snake_case(x) for x in reader.fieldnames] + ["source_extract_year"]
                    long_writer = csv.DictWriter(long_handle, fieldnames=long_fields)
                    long_writer.writeheader()

                for raw in reader:
                    key = (raw.get("Primary Key") or "").strip()
                    measure = (raw.get("Measure Names") or "").strip()
                    if key == "All":
                        excluded_summary_rows += 1
                        continue
                    if not key or not measure:
                        excluded_invalid_rows += 1
                        continue

                    normalized = {snake_case(k): v for k, v in raw.items() if k is not None}
                    normalized["source_extract_year"] = extract_year
                    long_writer.writerow(normalized)
                    long_rows += 1
                    annual_long_rows[extract_year] += 1
                    measure_counts[measure] += 1

                    if key not in transactions:
                        base = {
                            snake_case(k): v
                            for k, v in raw.items()
                            if k not in {"Measure Names", "Measure Values"} and k is not None
                        }
                        base["source_extract_year"] = extract_year
                        transactions[key] = base
                    transactions[key][snake_case(measure)] = raw.get("Measure Values", "")

    if len(schemas) != 1:
        raise RuntimeError(f"Annual schemas differ: {len(schemas)} variants found")

    base_fields = [
        snake_case(x)
        for x in next(iter(schemas))
        if x not in {"Measure Names", "Measure Values"}
    ]
    measure_fields = sorted({snake_case(x) for x in measure_counts})
    wide_fields = base_fields + ["source_extract_year"] + measure_fields
    with wide_path.open("w", encoding="utf-8", newline="") as wide_handle:
        writer = csv.DictWriter(wide_handle, fieldnames=wide_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(transactions.values())

    cost_complete = 0
    cost_within_one_percent = 0
    for row in transactions.values():
        try:
            quantity = float((row.get("pack_quantity") or "").replace(",", ""))
            unit_price = float((row.get("product_pack_usd") or "").replace(",", ""))
            total_cost = float((row.get("total_product_cost_usd") or "").replace(",", ""))
        except ValueError:
            continue
        cost_complete += 1
        relative_difference = abs(total_cost - quantity * unit_price) / max(abs(total_cost), 1e-12)
        if relative_difference <= 0.01:
            cost_within_one_percent += 1

    qa = {
        "extraction_date": "2026-09-11",
        "annual_files": len(files),
        "year_range": [2003, 2026],
        "schema_variants": len(schemas),
        "raw_long_rows_before_exclusions": long_rows + excluded_summary_rows + excluded_invalid_rows,
        "retained_long_rows": long_rows,
        "unique_transactions": len(transactions),
        "complete_numeric_cost_records": cost_complete,
        "cost_records_consistent_within_one_percent": cost_within_one_percent,
        "cost_records_outside_one_percent": cost_complete - cost_within_one_percent,
        "measure_counts": dict(measure_counts),
        "annual_retained_long_rows": dict(sorted(annual_long_rows.items())),
        "excluded_tableau_summary_rows": excluded_summary_rows,
        "excluded_invalid_rows": excluded_invalid_rows,
        "notes": [
            "The 2026 extract is a partial year as of the extraction date.",
            "Tableau returns three measure rows for most transactions; the ML-ready file pivots these measures to columns.",
            "Primary Key values equal to 'All' are Tableau summary rows and are excluded from derived datasets.",
            "The source is self-reported PQR data and remains subject to the Global Fund caveats note included with this package."
        ]
    }
    with qa_path.open("w", encoding="utf-8") as handle:
        json.dump(qa, handle, indent=2)

    print(json.dumps(qa, indent=2))


if __name__ == "__main__":
    main()
