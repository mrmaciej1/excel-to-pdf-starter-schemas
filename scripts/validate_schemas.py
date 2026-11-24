#!/usr/bin/env python3
"""Validate all CSV starter schemas and paired mapping artifacts in schemas/.

Checks performed on every schemas/**/*.csv:
  1. Strict UTF-8 decoding (no invalid bytes, no NUL bytes, no UTF-8 BOM).
  2. Non-empty header row, zero empty headers, no leading/trailing header spaces,
     and case-insensitive header uniqueness.
  3. At least 3 synthetic example rows and consistent column counts on every row.
  4. Paired documentation (.md) and machine-readable mapping (.mapping.json) exist.
  5. .mapping.json is valid JSON whose columns[].header list matches the CSV
     headers 1:1 in exact order and casing.
  6. Synthetic-data safety guard: verifies emails use @example.com / .example,
     SSN-shaped strings are synthetic (000-xx-xxxx, xxx-00-xxxx, or ***-**-xxxx),
     and US phone numbers stay inside the fictional 555-01xx block.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"

SSN_RE = re.compile(r"\b(\d{3})-(\d{2})-(\d{4})\b")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
PHONE_RE = re.compile(r"\(?\d{3}\)?[-.\s](\d{3})-(\d{4})\b")

EXPECTED_MIN_SCHEMAS = 9


def check_synthetic_cell(rel_path: str, row_num: int, header: str, value: str) -> list[str]:
    errors: list[str] = []

    for match in EMAIL_RE.finditer(value):
        domain = match.group(1).lower()
        if not (
            domain == "example.com"
            or domain.endswith(".example.com")
            or domain.endswith(".example")
        ):
            errors.append(
                f"{rel_path}:{row_num} [{header}] non-example email domain '{domain}'"
            )

    if "ssn" in header.lower() or "tin" in header.lower():
        for m in SSN_RE.finditer(value):
            area, group, _serial = m.groups()
            if area != "000" and group != "00":
                errors.append(
                    f"{rel_path}:{row_num} [{header}] SSN-like value '{m.group(0)}' "
                    f"must use synthetic area '000' or group '00'"
                )

    if "phone" in header.lower():
        for m in PHONE_RE.finditer(value):
            exchange, line = m.groups()
            if not (exchange == "555" and 100 <= int(line) <= 199):
                errors.append(
                    f"{rel_path}:{row_num} [{header}] phone '{m.group(0)}' "
                    f"must use fictional 555-0100..555-0199 range"
                )

    return errors


def validate_csv(csv_path: Path) -> tuple[list[str], dict[str, int | str]]:
    rel = csv_path.relative_to(ROOT).as_posix()
    errors: list[str] = []

    raw = csv_path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{rel}: contains UTF-8 BOM (save as plain UTF-8 without BOM)")
    if b"\x00" in raw:
        errors.append(f"{rel}: contains NUL byte")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"{rel}: invalid UTF-8: {exc}"], {"file": rel, "cols": 0, "rows": 0}

    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return [f"{rel}: file is empty"], {"file": rel, "cols": 0, "rows": 0}

    headers = rows[0]
    if not headers:
        errors.append(f"{rel}: header row is empty")

    seen_lower: set[str] = set()
    for idx, h in enumerate(headers, start=1):
        if not h or not h.strip():
            errors.append(f"{rel}: empty header at column {idx}")
            continue
        if h != h.strip():
            errors.append(f"{rel}: header '{h}' has leading or trailing whitespace")
        low = h.lower()
        if low in seen_lower:
            errors.append(f"{rel}: duplicate header (case-insensitive) '{h}'")
        seen_lower.add(low)

    data_rows = rows[1:]
    if len(data_rows) < 3:
        errors.append(f"{rel}: expected at least 3 synthetic example rows, found {len(data_rows)}")

    expected_cols = len(headers)
    for row_idx, row in enumerate(data_rows, start=2):
        if len(row) != expected_cols:
            errors.append(
                f"{rel}:{row_idx}: column count mismatch (expected {expected_cols}, got {len(row)})"
            )
            continue
        if all(cell.strip() == "" for cell in row):
            errors.append(f"{rel}:{row_idx}: completely blank data row")
        for col_idx, cell in enumerate(row):
            if cell != cell.strip():
                errors.append(
                    f"{rel}:{row_idx} [{headers[col_idx]}]: leading/trailing whitespace in '{cell}'"
                )
            errors.extend(check_synthetic_cell(rel, row_idx, headers[col_idx], cell))

    # Paired .md and .mapping.json checks
    md_path = csv_path.with_suffix(".md")
    if not md_path.is_file():
        errors.append(f"{rel}: missing paired documentation file '{md_path.name}'")
    elif md_path.stat().st_size < 200:
        errors.append(f"{rel}: paired documentation '{md_path.name}' looks unexpectedly short")

    mapping_path = csv_path.with_suffix(".mapping.json")
    if not mapping_path.is_file():
        errors.append(f"{rel}: missing paired mapping spec '{mapping_path.name}'")
    else:
        try:
            spec = json.loads(mapping_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON in '{mapping_path.name}': {exc}")
        else:
            for req_key in ("form_id", "official_title", "issuer", "pdf_architecture", "columns"):
                if req_key not in spec:
                    errors.append(f"{mapping_path.name}: missing required key '{req_key}'")
            cols = spec.get("columns")
            if not isinstance(cols, list):
                errors.append(f"{mapping_path.name}: 'columns' must be a list")
            else:
                spec_headers = [c.get("header") for c in cols if isinstance(c, dict)]
                if spec_headers != headers:
                    errors.append(
                        f"{rel}: CSV headers do not match {mapping_path.name} columns "
                        f"(csv={headers!r}, spec={spec_headers!r})"
                    )

    return errors, {"file": rel, "cols": expected_cols, "rows": len(data_rows)}


def main() -> int:
    if not SCHEMAS_DIR.is_dir():
        print(f"ERROR: schemas directory not found at {SCHEMAS_DIR}", file=sys.stderr)
        return 1

    csv_files = sorted(SCHEMAS_DIR.rglob("*.csv"))
    if len(csv_files) < EXPECTED_MIN_SCHEMAS:
        print(
            f"ERROR: expected at least {EXPECTED_MIN_SCHEMAS} CSV schemas, found {len(csv_files)}",
            file=sys.stderr,
        )
        return 1

    all_errors: list[str] = []
    summaries: list[dict[str, int | str]] = []

    for csv_path in csv_files:
        errs, summary = validate_csv(csv_path)
        all_errors.extend(errs)
        summaries.append(summary)

    print(f"Validated {len(csv_files)} CSV starter schemas:")
    print(f"{'Schema CSV':<56} {'Cols':>5} {'Rows':>5}  Status")
    print("-" * 78)
    for s in summaries:
        file_errs = [e for e in all_errors if e.startswith(str(s["file"]))]
        status = "OK" if not file_errs else f"FAIL ({len(file_errs)})"
        print(f"{str(s['file']):<56} {int(s['cols']):>5} {int(s['rows']):>5}  {status}")

    if all_errors:
        print("\nValidation errors:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"\nALL {len(csv_files)} SCHEMAS PASSED VALIDATION (UTF-8, headers, mappings, synthetic PII guard).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
