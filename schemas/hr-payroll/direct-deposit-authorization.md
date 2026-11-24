# Direct Deposit Authorization (ACH / Payroll Onboarding) — CSV Schema & Mapping Guide

- **Starter CSV:** [`direct-deposit-authorization.csv`](direct-deposit-authorization.csv)
- **Machine-Readable Spec:** [`direct-deposit-authorization.mapping.json`](direct-deposit-authorization.mapping.json)
- **Federal Reference Form:** U.S. Treasury **Form SF-1199A** (Rev. October 2024: 4 pages, 210 terminal fields, XFA Hybrid, `95.7%` readable field names — measured in the [JustFill 134-Form Study](https://justfill.app/research/are-government-forms-fillable))

> **Security & PII Best Practice:** All routing (`00000000x`) and account (`00012345678x`) numbers in `direct-deposit-authorization.csv` are non-routable synthetic placeholders. When testing any PDF merge pipeline, always calibrate field alignment with synthetic fixtures first, and in production consider pre-filling only employee/employer metadata while letting the employee enter banking details directly on an interactive form before signing.

## Column-to-Form Mapping

| CSV Header | Target Form Field | Formatting & Mapping Notes |
| ---------- | ----------------- | -------------------------- |
| `employee_id` | Employee / Payroll ID | Ideal for output filenames (`{employee_id}_{employee_last_name}_ACH.pdf`) |
| `employee_first_name`, `employee_last_name` | Employee Name (SF-1199A: `payname[0]`) | Concatenate if PDF uses a single full-name box |
| `employee_email` | Onboarding Email | Used for HR audit log or e-sign delivery |
| `employer_name` | Company Name | Lock as a batch constant |
| `action_type` | `New` / `Change` / `Cancel` checkboxes | Map enum string to PDF checkbox export values |
| `primary_bank_name` | Primary Financial Institution | Full bank or credit union name |
| `primary_routing_number` | 9-Digit ABA Routing Number | **Must be Text!** East Coast Fed districts (`01`–`09`) start with `0` |
| `primary_account_number` | Account Number | **Must be Text!** Preserves leading zeros and avoids Excel's 15-digit float precision limit |
| `primary_account_type` | `Checking` / `Savings` (SF-1199A: `xcheck[0]` / `xsvgs[0]`) | Mutually exclusive checkbox/radio group |
| `primary_deposit_allocation` | `100%` / `Remainder` / `$ Amount` | Use `Remainder` when a secondary split account is populated |
| `secondary_*` (5 columns) | Split Deposit Account 2 | Leave blank for single-account employees |
| `effective_date` | Effective Date | `MM/DD/YYYY` |

## Known Implementation Pitfalls

1. **Leading-Zero Stripping & 15-Digit Truncation in Excel:** ABA routing numbers starting with `0` (Boston, New York, Philadelphia, Cleveland, Richmond, Atlanta, Chicago, St. Louis, Minneapolis Fed districts) lose their leading zero if Excel parses the column as General/Number. Likewise, 16- or 17-digit bank account numbers have their final digits silently zeroed out by IEEE-754 double precision in Excel (`12345678901234567` → `12345678901234500`). Always store both columns as **Text (`@`)**.
2. **Per-Character Comb Boxes on Federal SF-1199A:** While most employer ACH forms use one text box for the account number, federal SF-1199A PDFs split the depositor account number into 17 individual character fields (`acct1[0]` through `acct17[0]`). Split the string character-by-character in your merge script or merge the comb boxes in your PDF tool.
3. **Flat Word-to-PDF Company Forms:** Most SMB HR direct-deposit sheets are flattened PDFs exported from Word or Google Docs with zero AcroForm fields. Inspect your form first at [justfill.app/pdf-form-fields](https://justfill.app/pdf-form-fields).

## Tools

- Inspect your company's ACH form or SF-1199A locally: [JustFill PDF Form Field Inspector](https://justfill.app/pdf-form-fields)
- Batch-fill HR onboarding packets (W-4, I-9, Direct Deposit) from Excel: [JustFill Excel-to-PDF Batch Fill](https://justfill.app/solutions/fill-pdf-from-excel)
- Managing tenant/residential onboarding packets too? See [JustFill Property Management Starter Kit](https://justfill.app/kits/property-management)
