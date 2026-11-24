# IRS Form W-9 (Rev. March 2024) — CSV Schema & AcroForm Mapping Guide

- **Starter CSV:** [`irs-w9.csv`](irs-w9.csv)
- **Machine-Readable Spec:** [`irs-w9.mapping.json`](irs-w9.mapping.json)
- **Official Blank PDF:** `https://www.irs.gov/pub/irs-pdf/fw9.pdf` (6 pages, 23 terminal fields on Page 1)
- **PDF Architecture:** **XFA Hybrid** (`Designer 6.5`, `0.0%` human-readable field names — measured in the [JustFill 134-Form Study](https://justfill.app/research/are-government-forms-fillable))

## Column-to-AcroForm Mapping

| CSV Header | Official IRS W-9 AcroForm Path | Widget Type | Formatting & Mapping Notes |
| ---------- | ------------------------------ | ----------- | -------------------------- |
| `Legal_Name` | `topmostSubform[0].Page1[0].f1_01[0]` | Text | Line 1 legal name |
| `Business_DBA_Name` | `topmostSubform[0].Page1[0].f1_02[0]` | Text | Line 2 business/disregarded entity name |
| `Tax_Classification` | `topmostSubform[0].Page1[0].Boxes3a-b_ReadOrder[0].c1_1[0..6]` | Checkbox | Export values: `/1` Ind/Sole Prop, `/2` C Corp, `/3` S Corp, `/4` Partnership, `/5` Trust/Estate, `/6` LLC, `/7` Other |
| `LLC_Tax_Code` | `topmostSubform[0].Page1[0].Boxes3a-b_ReadOrder[0].f1_03[0]` | Text | `C`, `S`, or `P` when `c1_1[5]` (`/6`) is checked |
| `Foreign_Partners_Line_3b` | `topmostSubform[0].Page1[0].Boxes3a-b_ReadOrder[0].c1_2[0]` | Checkbox | Added in Rev. March 2024; export value `/1` or `/Off` |
| `Exempt_Payee_Code` | `topmostSubform[0].Page1[0].f1_05[0]` | Text | Line 4 code (1–13) |
| `FATCA_Exemption_Code` | `topmostSubform[0].Page1[0].f1_06[0]` | Text | Line 4 code (A–M) |
| `Street_Address` | `topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_07[0]` | Text | Line 5 street address |
| `City_State_ZIP` | `topmostSubform[0].Page1[0].Address_ReadOrder[0].f1_08[0]` | Text | Line 6 city, state, ZIP (`02110`, `07102` keep leading zeros) |
| `Requester_Name_and_Address` | `topmostSubform[0].Page1[0].f1_09[0]` | Text | Optional requester block (often constant across batch) |
| `Account_Number` | `topmostSubform[0].Page1[0].f1_10[0]` | Text | Line 7 account / vendor ID |
| `TIN_Type` | *(routing helper)* | — | `EIN` or `SSN` to route Part I fields |
| `EIN_Prefix` | `topmostSubform[0].Page1[0].f1_14[0]` | Text (comb, 2) | First 2 EIN digits (keep as text) |
| `EIN_Suffix` | `topmostSubform[0].Page1[0].f1_15[0]` | Text (comb, 7) | Last 7 EIN digits (keep as text) |
| `SSN_Placeholder` | `f1_11[0]`, `f1_12[0]`, `f1_13[0]` | Text (3+2+4) | Split on `-` into 3 Part I SSN comb fields, or omit so vendor completes |

## Known Implementation Pitfalls

1. **XFA Hybrid Drift:** `fw9.pdf` includes an `/XFA` XML stream. If your script fills AcroForm fields without stripping `/XFA` or setting appearance streams properly, Adobe Acrobat Reader may display blank values while Chrome/Preview show filled values.
2. **Split TIN Comb Boxes:** Do not map a 9-digit EIN (`12-3456789`) into a single field; W-9 separates `f1_14[0]` (2 chars) and `f1_15[0]` (7 chars), and splits SSN across `f1_11[0]` (3), `f1_12[0]` (2), and `f1_13[0]` (4).
3. **Pre-fill Workflow Best Practice:** Accounts payable teams often leave `EIN_*` / `SSN_Placeholder` blank and pre-fill Lines 1–7, then send the draft to the vendor to confirm their TIN and sign Part II.

## Tools

- Inspect `fw9.pdf` locally in your browser: [JustFill PDF Form Field Inspector](https://justfill.app/pdf-form-fields)
- Ready-made `.xlsx` QuickBooks-aligned kit: [JustFill CPA & Tax Firms Starter Kit](https://justfill.app/kits/cpa-tax-firms)
