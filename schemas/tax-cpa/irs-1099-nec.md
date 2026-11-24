# IRS Form 1099-NEC — CSV Schema & AcroForm Mapping Guide

- **Starter CSV:** [`irs-1099-nec.csv`](irs-1099-nec.csv)
- **Machine-Readable Spec:** [`irs-1099-nec.mapping.json`](irs-1099-nec.mapping.json)
- **Official Blank PDF:** `https://www.irs.gov/pub/irs-pdf/f1099nec.pdf` (6 pages, 140 terminal fields across Copy A, Copy 1, Copy B, and Copy 2)
- **PDF Architecture:** **XFA Hybrid** (`Designer 6.5`, `0.0%` human-readable field names — measured in the [JustFill 134-Form Study](https://justfill.app/research/are-government-forms-fillable))

> **Filing Compliance Note:** The IRS prohibits filing Copy A printed from the downloadable PDF on paper (paper Copy A requires official red-ink OCR scannable forms, and most filers with 10+ total returns must e-file via IRS IRIS/FIRE). Use PDF mail merge for **Copy B (Recipient)**, **Copy 2 (Recipient State)**, **Copy 1 (State)**, and **Payer file copies / review drafts**.

## Column-to-AcroForm Mapping

Because `f1099nec.pdf` bundles multiple copies (`CopyA[0]`, `Copy1[0]`, `CopyB[0]`, `Copy2[0]`) with XFA auto-sync scripts that do **not** run in headless `pypdf`/`pdf-lib` batch pipelines, batch scripts targeting `CopyB` / `Copy1` / `Copy2` must write explicitly to each target copy's page fields (example below shows `Copy1[0]` prefixes):

| CSV Header | Example AcroForm Field (`Copy1[0]`) | Notes |
| ---------- | ----------------------------------- | ----- |
| `Tax_Year` | `PgHeader[0].CalendarYear[0].f2_1[0]` | Tax year printed in header |
| `Payer_Name_and_Address` | `LeftCol[0].f2_2[0]` | Combine or split across address sub-lines depending on PDF revision |
| `Payer_Phone` | `LeftCol[0].f2_2[0]` | Included in Payer block |
| `Payer_TIN` | `LeftCol[0].f2_10[0]` | Keep hyphenated (`XX-XXXXXXX`) |
| `Recipient_TIN` | `LeftCol[0].f2_11[0]` | Supports IRS-permitted TTIN (`***-**-0001`) on recipient Copy B |
| `Recipient_Name` | `LeftCol[0].f2_12[0]` | Legal name from W-9 |
| `Recipient_Street_Address` | `LeftCol[0].f2_13[0]` | Street & suite |
| `Recipient_City_State_ZIP` | `LeftCol[0].f2_16[0]` | Preserve leading-zero ZIP codes |
| `Account_Number` | `LeftCol[0].f2_19[0]` | Vendor/ledger ID |
| `Box_1_Nonemployee_Compensation` | `RightCol[0].f2_20[0]` | Omit `$` sign (pre-printed on form) |
| `Box_2_Direct_Sales_5000_Checkbox` | `RightCol[0].c1_3[0]` | Checkbox export `/1` or `/Off` |
| `Box_4_Federal_Income_Tax_Withheld` | `RightCol[0].f2_25[0]` | Decimal without `$` |
| `Box_5_State_Tax_Withheld` | `RightCol[0].Box5_ReadOrder[0].f2_27[0]` | State withholding line 1 |
| `Box_6_State_Payer_State_No` | `RightCol[0].Box6_ReadOrder[0].f2_29[0]` | State abbreviation / payer state ID |
| `Box_7_State_Income` | `RightCol[0].f2_31[0]` | State income line 1 |
| `Corrected_Return` | `PgHeader[0].c2_1[1]` | Checkbox export `/2` or `/Off` |

## Known Implementation Pitfalls

1. **XFA Copy-Propagation Doesn't Execute Server-Side:** In Adobe Reader, typing into Copy A mirrors values into Copy 1/B/2 via LiveCycle JavaScript. In Python/Node batch scripts, you must populate the target copy (`CopyB[0]`, `Copy1[0]`, `Copy2[0]`) directly and extract only the non-Copy-A pages if distributing to recipients.
2. **Double Dollar Signs:** Box 1, Box 4, Box 5, and Box 7 have pre-printed `$` symbols on the form. Pass clean decimal numbers (`18450.00`) rather than `$18,450.00` unless your pipeline strips currency characters.
3. **Revision Drift:** IRS updated Form 1099-NEC field counts across editions (including the 2026 revision adding Box 1b sub-fields). Always inspect your exact year's PDF first with [justfill.app/pdf-form-fields](https://justfill.app/pdf-form-fields).

## Tools

- Batch-fill 1099-NEC Copy B/C/1/2 from QuickBooks/Excel: [JustFill Excel-to-PDF Batch Fill](https://justfill.app/solutions/fill-pdf-from-excel)
- CPA & Tax Firms starter workbook: [JustFill CPA & Tax Firms Starter Kit](https://justfill.app/kits/cpa-tax-firms)
