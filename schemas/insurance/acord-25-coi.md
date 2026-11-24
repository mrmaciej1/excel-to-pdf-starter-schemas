# ACORD 25 Certificate of Liability Insurance (COI) — CSV Schema & Mapping Guide

- **Starter CSV:** [`acord-25-coi.csv`](acord-25-coi.csv)
- **Machine-Readable Spec:** [`acord-25-coi.mapping.json`](acord-25-coi.mapping.json)
- **Typical Source Systems:** Applied Epic, Vertafore AMS360, HawkSoft, EZLynx, or contractor Excel holder schedules

> **ACORD Licensing Notice:** ACORD® forms are copyrighted by ACORD Corporation. This repository provides spreadsheet schemas and mapping documentation only—never blank ACORD PDFs. Upload your agency's own licensed ACORD 25 PDF exported from your AMS or ACORD subscription.

## Column-to-ACORD 25 Block Mapping

| CSV Header | ACORD 25 Section | Mapping & Batch Notes |
| ---------- | ---------------- | --------------------- |
| `certificate_date` | Top-Right `DATE (MM/DD/YYYY)` | Usually constant across a renewal run |
| `producer_name`, `producer_address`, `producer_phone`, `producer_email` | `PRODUCER` & Contact Block | Lock once on your saved agency template |
| `insured_name`, `insured_address` | `INSURED` Block | Matches Named Insured on underlying policies |
| `insurer_a_name`, `insurer_a_naic` | `INSURERS AFFORDING COVERAGE` | Keep 5-digit NAIC code as Text so leading zeros stay intact |
| `gl_policy_number`, `gl_effective_date`, `gl_expiration_date` | `COVERAGES` (Commercial General Liability) | Update dates/numbers once in Excel at annual renewal |
| `each_occurrence_limit`, `general_aggregate_limit` | `LIMITS` Column | Watch horizontal overflow inside narrow currency cells |
| `additional_insured_flag`, `waiver_of_subrogation_flag` | `ADDL INSD` / `SUBR WVD` | Single character `Y` / `N` or blank |
| `description_of_operations` | `DESCRIPTION OF OPERATIONS / LOCATIONS / VEHICLES` | Multiline field; enable word-wrap and check font scaling |
| `certificate_holder_name`, `certificate_holder_address`, `certificate_holder_city_state_zip` | `CERTIFICATE HOLDER` (Bottom Left) | One row per holder → one standalone COI PDF |

## Known Implementation Pitfalls

1. **Flat AMS Exports:** Many agency management systems export ACORD 25 templates as flattened PDFs (zero AcroForm fields). Check your file first in [justfill.app/pdf-form-fields](https://justfill.app/pdf-form-fields); if flat, use visual AI field detection rather than hand-drawing 60+ narrow boxes.
2. **Narrow Limit & NAIC Columns:** Default 12pt AcroForm fonts clip `$1,000,000` and 5-digit NAIC codes inside the Coverages table. Set 7pt–8.5pt auto-fit fonts on table cells and verify every draft before distribution.
3. **Additional Lines of Coverage:** Extend this base CGL schema by duplicating the pattern (`auto_policy_number`, `umbrella_policy_number`, `wc_policy_number`) when your account carries Auto, Umbrella, and Workers' Compensation.

## Tools

- Inspect your licensed ACORD 25 PDF locally: [JustFill PDF Form Field Inspector](https://justfill.app/pdf-form-fields)
- Batch-generate holder COIs & renewal kits: [Commercial Insurance ACORD Starter Kit](https://justfill.app/kits/commercial-insurance-acord) · [Excel-to-PDF Batch Fill](https://justfill.app/solutions/fill-pdf-from-excel)
