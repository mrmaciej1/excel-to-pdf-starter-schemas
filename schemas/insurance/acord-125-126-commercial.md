# ACORD 125 & ACORD 126 (Commercial Application & CGL) — CSV Schema & Mapping Guide

- **Starter CSV:** [`acord-125-126-commercial.csv`](acord-125-126-commercial.csv)
- **Machine-Readable Spec:** [`acord-125-126-commercial.mapping.json`](acord-125-126-commercial.mapping.json)
- **Typical Source Systems:** Applied Epic CSV, Vertafore AMS360, HawkSoft, EZLynx, or Insured Statement of Values (SOV) Excel sheets

> **ACORD Licensing Notice:** ACORD® is a registered trademark of ACORD Corporation. This repository distributes CSV column schemas and field-mapping notes only—never blank copyrighted ACORD PDFs. Always use your agency's own licensed ACORD 125, 126, and 140 PDFs.

## Multi-Form Packet Architecture (125 + 126 + 140)

Commercial lines submissions routinely combine **ACORD 125** (Applicant Information), **ACORD 126** (Commercial General Liability Section), and **ACORD 140** (Commercial Property Section). Keeping shared column headers (`Named_Insured`, `Policy_Number`, `Effective_Date`, `Expiration_Date`, `Agency_Name`, `Carrier_or_MGA`, `Premises_Address`) lets one AMS or SOV spreadsheet feed all three forms without re-keying:

| CSV Header | Target ACORD Form(s) | Section & Field Notes |
| ---------- | -------------------- | --------------------- |
| `Named_Insured`, `DBA_Name`, `FEIN`, `NAICS_Code` | ACORD 125 / 126 / 140 | Applicant header; repeated on every page header |
| `Policy_Number`, `Effective_Date`, `Expiration_Date` | ACORD 125 / 126 / 140 | Policy term dates in `MM/DD/YYYY` |
| `Agency_Name`, `Account_Manager`, `Carrier_or_MGA` | ACORD 125 / 126 / 140 | Producer & market marketing block |
| `Line_of_Business` | ACORD 125 | Maps to Lines of Business checkboxes & submission summary |
| `Premises_Address` | ACORD 125 & 140 | Location / building schedule row |
| `GL_Class_Code`, `GL_Exposure_Basis` | ACORD 126 | Schedule of Hazards (5-digit ISO class code + sales/payroll/area basis) |
| `Each_Occurrence_Limit`, `General_Aggregate_Limit` | ACORD 126 | Commercial General Liability limits |
| `Building_Limit`, `BPP_Limit` | ACORD 140 | Subject of Insurance limits from Statement of Values (SOV) |

## Known Implementation Pitfalls

1. **Dense 150–300+ Field Multi-Page PDFs:** Carrier supplemental applications and older ACORD 125/126 PDFs are often flattened exports or inconsistently named AcroForms across editions. Inspect your exact file locally with [justfill.app/pdf-form-fields](https://justfill.app/pdf-form-fields) before hard-coding field names.
2. **SOV Row Fan-Out vs. Account Fan-Out:** Decide whether each CSV row represents one **insured account** (renewal book batch) or one **building/location** (20–200 row Statement of Values mapped onto ACORD 140 / ACORD 101 overflow pages).
3. **Currency & Leading Zeros:** Format `FEIN`, `NAICS_Code`, and East Coast `Premises_Address` ZIP codes (`02110`, `07102`) as Text so Excel never strips leading zeros.

## Tools

- Ready-to-download `.xlsx` workbook & live batch demo: [JustFill Commercial Insurance ACORD Starter Kit](https://justfill.app/kits/commercial-insurance-acord)
- Online Excel-to-PDF mail merge for flat or fillable ACORD PDFs: [JustFill Fill PDF from Excel](https://justfill.app/solutions/fill-pdf-from-excel)
