# Texas Form 01-339 (Sales & Use Tax Resale Certificate) — CSV Schema & Mapping Guide

- **Starter CSV:** [`tx-01-339-resale-certificate.csv`](tx-01-339-resale-certificate.csv)
- **Machine-Readable Spec:** [`tx-01-339-resale-certificate.mapping.json`](tx-01-339-resale-certificate.mapping.json)
- **Official Blank PDF:** `https://comptroller.texas.gov/forms/01-339.pdf` (2 pages: Page 1 = Resale Certificate, Page 2 = Exemption Certificate)
- **Primary B2B Use Case:** Wholesale distributors, manufacturers, and B2B credit desks pre-filling resale certificates during customer onboarding or annual tax-exemption renewal audits.

## Column-to-Form Mapping (Page 1 — Resale Certificate)

| CSV Header | Form 01-339 Field | Notes |
| ---------- | ----------------- | ----- |
| `purchaser_name`, `purchaser_phone` | Name of purchaser & Phone | Must match Texas Sales & Use Tax Permit |
| `purchaser_street_address`, `purchaser_city_state_zip` | Purchaser Address / City, State, ZIP | Keep ZIP as Text |
| `texas_taxpayer_number` | 11-digit Texas Taxpayer Number | **Text-formatted!** Excel turns unformatted 11-digit IDs into `3.00E+10` |
| `out_of_state_registration_number`, `out_of_state_jurisdiction` | Out-of-state retailer registration | Populated only when purchaser holds no Texas permit |
| `seller_name`, `seller_street_address`, `seller_city_state_zip` | Seller block | Commonly locked to your wholesale/distributor entity across all rows |
| `items_to_be_purchased_description` | Description of items to be purchased | Multiline description (check wrap/overflow) |
| `purchaser_business_activity_description` | Business activity / items normally sold | Multiline description required for valid resale claim |
| `authorized_signer_name`, `authorized_signer_title`, `certificate_date` | Signature / Title / Date block | Leave wet/e-signature blank until purchaser verifies and signs |

## Known Implementation Pitfalls

1. **Excel Scientific Notation on 11-Digit Permit Numbers:** Texas Taxpayer Numbers are 11 digits (e.g., `30000000001`). Opening raw CSVs directly in Excel converts 11+ digit numbers into scientific notation (`3E+10`) and silently corrupts the last digits upon re-save. Import via **Data → From Text/CSV** with Text column type, or use a Text `@` `.xlsx` template.
2. **Resale (Page 1) vs. Exemption (Page 2):** `01-339.pdf` bundles both certificates in one file. Wholesale buyers purchasing inventory for resale complete **Page 1 only**; tax-exempt nonprofits/schools/manufacturers claiming an exempt-use reason complete **Page 2**. Extract Page 1 if sending resale packets to commercial buyers so signers don't fill the wrong page.
3. **Retention & Verification:** Under Texas Comptroller rules, the seller retains the signed certificate (do not mail it to the Comptroller) and should verify the 11-digit permit status via the Texas Comptroller's online taxpayer search.

## Tools

- Inspect `01-339.pdf` AcroForm fields locally: [JustFill PDF Form Field Inspector](https://justfill.app/pdf-form-fields)
- Batch pre-fill B2B vendor/customer packets from Excel/CSV: [JustFill Excel-to-PDF Batch Fill](https://justfill.app/solutions/fill-pdf-from-excel)
