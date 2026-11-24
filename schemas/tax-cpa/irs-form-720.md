# IRS Form 720 (Quarterly Federal Excise Tax / Q2 PCORI) — CSV Schema & Mapping Guide

- **Starter CSV:** [`irs-form-720.csv`](irs-form-720.csv)
- **Machine-Readable Spec:** [`irs-form-720.mapping.json`](irs-form-720.mapping.json)
- **Official Blank PDF:** `https://www.irs.gov/pub/irs-pdf/f720.pdf` (Multi-page XFA Hybrid)
- **Primary B2B Batch Use Case:** CPA firms and benefits brokers preparing dozens of **Q2 PCORI fee** filings (Part II, IRS No. 133, due July 31 each year) for SMB clients sponsoring self-insured health plans, level-funded plans, or HRAs.

> **Rate Verification Note:** The IRS adjusts the PCORI fee rate annually based on the policy/plan year end date (and updates Form 720 quarterly revisions). Values in `irs-form-720.csv` are synthetic examples—always verify the exact rate and current quarter revision of `f720.pdf` before filing.

## Column-to-Form Mapping Overview

| CSV Header | Form 720 Section | Formatting & Mapping Notes |
| ---------- | ---------------- | -------------------------- |
| `Taxpayer_Name`, `Trade_Name_DBA`, `EIN` | Page 1 Header | EIN formatted `XX-XXXXXXX`; repeats on Page 2+ headers in batch scripts |
| `Street_Address`, `City_State_ZIP` | Page 1 Header | Preserve leading-zero ZIP codes (`07102`) |
| `Quarter_Ending` | Page 1 Header | `06/30/YYYY` for annual PCORI fee returns |
| `Final_Return_Checkbox`, `Address_Change_Checkbox` | Page 1 Header | Map to header checkboxes |
| `IRS_No`, `Excise_Tax_Category` | Part I / Part II Router | `133` routes to Part II PCORI (specified health insurance / self-insured plans) |
| `Avg_Covered_Lives_or_Units`, `Applicable_Rate` | Part II IRS No. 133 cols (a)/(b) | Keep rate to 2 decimal places (`3.47` example) |
| `Part_I_Total_Tax`, `Part_II_Total_Tax` | Part I Line 1 / Part II Line 2 | Decimal strings without `$` |
| `Part_III_Line_3_Total_Tax`, `Schedule_C_Claims_Line_4`, `Deposits_Line_6`, `Balance_Due_Line_10` | Part III Lines 3–10 | Carry `Balance_Due_Line_10` to Form 720-V voucher if paying by check |
| `Third_Party_Designee_Name`, `Paid_Preparer_PTIN` | Part III Signature / Paid Preparer | Typically constant across a CPA firm's client batch |

## Known Implementation Pitfalls

1. **Quarterly IRS Revisions Shift `f1_xx[0]` Indexes:** Form 720 is revised frequently (adding/expiring excise lines), which renumbers LiveCycle `f1_*` and `f2_*` field IDs. Inspect the exact quarterly `f720.pdf` you download with [justfill.app/pdf-form-fields](https://justfill.app/pdf-form-fields) before reusing an automated script.
2. **Repeated Entity Header Across Pages:** In `pypdf` / `pdf-lib` batch fills, XFA auto-copy from Page 1 Name/EIN to Page 2/3/720-V headers will not run automatically; map `Taxpayer_Name` and `EIN` onto every page header widget explicitly.
3. **Two PCORI Rows Under IRS No. 133:** Part II IRS No. 133 splits plan years ending **before October 1** vs. **on or after October 1** (which can carry different statutory per-life rates). Confirm which row matches each client's plan year end.

## Tools

- Inspect the current quarter's `f720.pdf` fields in your browser: [JustFill PDF Form Field Inspector](https://justfill.app/pdf-form-fields)
- Batch-fill client Form 720 packets from Excel: [JustFill Excel-to-PDF Batch Fill](https://justfill.app/solutions/fill-pdf-from-excel) · [CPA & Tax Firms Starter Kit](https://justfill.app/kits/cpa-tax-firms)
