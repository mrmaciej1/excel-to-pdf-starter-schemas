# Excel-to-PDF Starter Schemas

[![Validate Schemas](https://github.com/mrmaciej1/excel-to-pdf-starter-schemas/actions/workflows/validate.yml/badge.svg)](https://github.com/mrmaciej1/excel-to-pdf-starter-schemas/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Practical, MIT-licensed **CSV column starter schemas**, **machine-readable `.mapping.json` specs**, and **AcroForm / XFA field-mapping notes** for batch-populating high-frequency B2B, tax, insurance, DMV, wholesale, and HR PDF forms from Excel or CSV.

Built for developers wiring PDF mail-merge pipelines (`pypdf`, `pdf-lib`, `pdftk`, `PyMuPDF`, n8n) and B2B operations teams exporting spreadsheets from QuickBooks, Applied Epic / AMS360, dealer DMS tools, and payroll / HRIS platforms.

> **Synthetic data only:** Every row in this repository uses strictly synthetic placeholder fixtures (e.g., `Acme Plumbing LLC`, `Jane Doe`, `12-3456789`, `000-00-0001`, `@example.com`, `555-01xx`). Never commit real taxpayer, employee, bank, or policyholder PII.

---

## Starter Schema Catalog (9 Ready-to-Use CSVs)

Each CSV ships with realistic synthetic rows, a human-readable `.md` mapping guide, and a validated `.mapping.json` column specification:

| # | Vertical | Form | Starter CSV | Mapping Guide & JSON Spec | PDF Architecture & Key Gotchas |
| - | -------- | ---- | ----------- | ------------------------- | ------------------------------ |
| 1 | Tax & CPA | **IRS Form W-9** (Rev. March 2024) | [`irs-w9.csv`](schemas/tax-cpa/irs-w9.csv) | [Guide](schemas/tax-cpa/irs-w9.md) · [JSON](schemas/tax-cpa/irs-w9.mapping.json) | XFA hybrid (23 fields); `0.0%` readable names (`f1_01[0]`–`f1_15[0]`); split EIN/SSN comb boxes; checkboxes use `/1`–`/7` |
| 2 | Tax & CPA | **IRS Form 1099-NEC** (Copy B/C/1/2) | [`irs-1099-nec.csv`](schemas/tax-cpa/irs-1099-nec.csv) | [Guide](schemas/tax-cpa/irs-1099-nec.md) · [JSON](schemas/tax-cpa/irs-1099-nec.mapping.json) | XFA hybrid (140 fields across copies); `0.0%` readable names (`Copy1[0].LeftCol[0].f2_2[0]`); never paper-file PDF Copy A |
| 3 | Tax & CPA | **IRS Form 1095-C** (ACA Employer) | [`irs-1095-c.csv`](schemas/tax-cpa/irs-1095-c.csv) | [Guide](schemas/tax-cpa/irs-1095-c.md) · [JSON](schemas/tax-cpa/irs-1095-c.mapping.json) | XFA hybrid (306 terminal fields); `f1_1[0]`–`f1_44[0]`; leading zeros in `Plan_Start_Month` (`01`) and `ZIP` (`02110`) |
| 4 | Tax & CPA | **IRS Form 720** (Quarterly Excise / PCORI) | [`irs-form-720.csv`](schemas/tax-cpa/irs-form-720.csv) | [Guide](schemas/tax-cpa/irs-form-720.md) · [JSON](schemas/tax-cpa/irs-form-720.mapping.json) | Multi-page XFA hybrid; IRS No. line codes (e.g., `133` for Q2 PCORI filings); verify current plan-year rates |
| 5 | Insurance | **ACORD 25** (Certificate of Liability Insurance) | [`acord-25-coi.csv`](schemas/insurance/acord-25-coi.csv) | [Guide](schemas/insurance/acord-25-coi.md) · [JSON](schemas/insurance/acord-25-coi.mapping.json) | Dense policy & NAIC grid; often flat/scanned from AMS exports; bring your agency's own licensed ACORD PDF |
| 6 | Insurance | **ACORD 125 / 126** (Commercial App & CGL) | [`acord-125-126-commercial.csv`](schemas/insurance/acord-125-126-commercial.csv) | [Guide](schemas/insurance/acord-125-126-commercial.md) · [JSON](schemas/insurance/acord-125-126-commercial.mapping.json) | 100+ dense fields & SOV location schedules; shared `Named_Insured`/`FEIN` headers across 125/126/140 packets |
| 7 | Automotive Sales | **Texas Form 130-U** (Title & Registration) | [`tx-130-u-title-transfer.csv`](schemas/automotive-sales/tx-130-u-title-transfer.csv) | [Guide](schemas/automotive-sales/tx-130-u-title-transfer.md) · [JSON](schemas/automotive-sales/tx-130-u-title-transfer.mapping.json) | Plain AcroForm (106 fields, `96.2%` named), encrypted (`modifyDenied` & `annotateDenied`), 17-char VIN comb box |
| 8 | B2B Wholesale | **Texas Form 01-339** (Resale Certificate) | [`tx-01-339-resale-certificate.csv`](schemas/b2b-wholesale/tx-01-339-resale-certificate.csv) | [Guide](schemas/b2b-wholesale/tx-01-339-resale-certificate.md) · [JSON](schemas/b2b-wholesale/tx-01-339-resale-certificate.mapping.json) | 11-digit Texas Taxpayer Number turns into `3E+10` in Excel without Text `@` formatting; front (Resale) vs. back (Exemption) |
| 9 | HR & Payroll | **Direct Deposit Authorization** (ACH / SF-1199A) | [`direct-deposit-authorization.csv`](schemas/hr-payroll/direct-deposit-authorization.csv) | [Guide](schemas/hr-payroll/direct-deposit-authorization.md) · [JSON](schemas/hr-payroll/direct-deposit-authorization.mapping.json) | 9-digit ABA routing numbers with leading zeros (`01`–`09` Fed districts); split account comb boxes (`acct1[0]`–`acct17[0]` on SF-1199A) |

---

## Why Excel-to-PDF Batch Pipelines Break (AcroForm vs. XFA Pitfalls)

When automating PDF form fills from spreadsheets, **"fillable" and "mappable" are two very different properties.**

In our structural study of **134 official government form entries** (133 unique PDFs, published under **CC BY 4.0** at [justfill.app/research/are-government-forms-fillable](https://justfill.app/research/are-government-forms-fillable)):

- **85.1% are XFA hybrids (114 of 134 analyzed forms):** 67 of 68 IRS forms, 24 of 26 USCIS forms, 10 of 13 California court forms, and every SSA and VA form tested ship an Adobe LiveCycle `/XFA` XML packet alongside AcroForm widgets (116 of 134 declare Adobe LiveCycle / Designer as producer). Only 15 of 134 (11.2%) are plain AcroForms, and 5 of 134 (3.7%) are completely flat PDFs with zero widgets.
- **61 IRS forms use opaque field codes instead of words:** 63 of 129 fillable forms (48.8%) have fewer than 10% human-readable field names—and **61 of those 63 are IRS forms** whose AcroForm names look like `topmostSubform[0].Page1[0].f1_01[0]`, `f1_1[0]`, and `c1_1[0]`.
- **33.6% carry owner encryption flags (45 of 134):** All 45 permit filling, while 44 deny document modification and 16 deny annotations (including Texas Form 130-U). Libraries that rewrite the PDF catalog without respecting permission bits or clearing `/XFA` can trigger viewer warnings or blank field appearances.
- **Median fillable form has 91 fields** (19,512 terminal fields across 129 fillable forms: 14,207 text, 5,029 checkboxes, 202 dropdowns, 58 radio groups, and 16 signature fields).

### Top 5 Engineering & Ops Pitfalls (and How These Schemas Avoid Them)

1. **XFA / AcroForm divergence:** Writing values only into the `/AcroForm` dictionary while leaving an embedded `/XFA` stream intact causes Adobe Acrobat / Reader to render stale or blank values from the XML layer while Chrome/Preview show the AcroForm layer. Always inspect whether `/XFA` is present before running a batch script.
2. **Opaque IRS field paths (`f1_1[0]`):** Keep your business spreadsheet headers human-readable (`Legal_Name`, `Line14_All_12_Months`) and store the PDF target path in a separate mapping layer (see each schema's `.mapping.json` and `.md` guide).
3. **Excel corrupting leading zeros & long IDs:** Opening raw CSVs by double-clicking in Excel strips leading zeros from East Coast ZIPs (`02110` → `2110`), ACA `Plan_Start_Month` (`01` → `1`), and ABA routing numbers (`010000001` → `10000001`), and converts 11-digit Texas Taxpayer Numbers into scientific notation (`3.00E+10`). Import via **Data → From Text/CSV** (UTF-8, Text type) or generate a Text-formatted `@` `.xlsx` workbook.
4. **Split comb boxes (TINs, VINs, account numbers):** Official PDFs frequently break one identifier across multiple AcroForm fields—for example, IRS W-9 splits EIN into `f1_14[0]` (2 digits) + `f1_15[0]` (7 digits) and SSN into `f1_11[0]` / `f1_12[0]` / `f1_13[0]`, while Federal SF-1199A splits account numbers into `acct1[0]` through `acct17[0]`.
5. **Non-boolean checkbox export values:** PDF checkboxes rarely use `"true"`/`"false"`. On IRS W-9 (Rev. March 2024), the 7 tax-classification widgets (`c1_1[0]`..`c1_1[6]`) use export values `/1` through `/7` (and `/Off` when unchecked).

---

## Quickstart

### 1. Inspect Your Own PDF's Exact Field Names First

Before wiring a CSV to any PDF, inspect its real AcroForm field tree, checkbox export values, page rects, and XFA status:

- **Free local browser inspector (no upload):** Drop any PDF into [justfill.app/pdf-form-fields](https://justfill.app/pdf-form-fields) to inspect every AcroForm/XFA field locally via `pdf.js` + `pdf-lib`, check for hidden/read-only/XFA traps, and export a ready-to-fill `.xlsx` template with Text `@` formatting.
- **No-code Excel/CSV batch fill:** To merge any of these starter CSVs directly onto fillable, XFA, or flat/scanned PDFs in the browser (with visual canvas review and ZIP export), see [justfill.app/solutions/fill-pdf-from-excel](https://justfill.app/solutions/fill-pdf-from-excel).

### 2. Validate Schemas Locally

Requires Python 3.9+ (standard library only, zero third-party dependencies):

```bash
python3 scripts/validate_schemas.py
```

The validator checks every `schemas/**/*.csv` for:
- Strict UTF-8 decoding (no NUL bytes, no stray BOM)
- Non-empty, unique, whitespace-trimmed headers
- Consistent column counts across every row
- 1:1 header alignment with the paired `.mapping.json` file and presence of the `.md` guide
- Synthetic-data safety checks (flags real-looking SSNs, non-`@example.com` emails, or non-`555-01xx` phone numbers)

---

## Related Vertical Starter Kits & Open Research

- **134-Form Government PDF Fillability Study (CC BY 4.0 CSV & methodology):** [justfill.app/research/are-government-forms-fillable](https://justfill.app/research/are-government-forms-fillable)
- **CPA & Tax Firms Starter Kit** (QuickBooks CSV → W-9, 1099-NEC, 1095-C, Form 8879): [justfill.app/kits/cpa-tax-firms](https://justfill.app/kits/cpa-tax-firms)
- **Commercial Insurance ACORD Starter Kit** (Applied Epic / AMS360 / SOV Excel → ACORD 25, 125/126/140): [justfill.app/kits/commercial-insurance-acord](https://justfill.app/kits/commercial-insurance-acord)
- **Property Management Starter Kit** (AppFolio / Buildium / Yardi rent rolls → Lease Renewals & Rent Notices): [justfill.app/kits/property-management](https://justfill.app/kits/property-management)

---

## Compliance & Trademark Notice

- This repository distributes **spreadsheet column schemas and field-mapping documentation only**—it does **not** host, redistribute, or license blank copyrighted ACORD® PDFs or provide tax, accounting, insurance, or legal advice.
- Always upload your organization's own current official government PDFs or licensed ACORD® forms and verify current-year instructions and rates before filing.
- ACORD® is a registered trademark of ACORD Corporation. QuickBooks, Applied Epic, AMS360, AppFolio, Buildium, Yardi, Adobe, and Microsoft Excel are trademarks of their respective owners.

## License

MIT — see [LICENSE](LICENSE). Contributions of additional synthetic starter schemas and AcroForm mapping guides are welcome via pull request (run `python3 scripts/validate_schemas.py` before opening a PR).
