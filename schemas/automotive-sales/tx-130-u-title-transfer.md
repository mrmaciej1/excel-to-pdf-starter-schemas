# Texas Form 130-U (Title & Registration) — CSV Schema & AcroForm Mapping Guide

- **Starter CSV:** [`tx-130-u-title-transfer.csv`](tx-130-u-title-transfer.csv)
- **Machine-Readable Spec:** [`tx-130-u-title-transfer.mapping.json`](tx-130-u-title-transfer.mapping.json)
- **Official Blank PDF:** `https://www.txdmv.gov/sites/default/files/form_files/Form-130-U.pdf` (2 pages, 106 terminal fields: 55 text, 48 checkboxes, 3 signatures)
- **PDF Architecture:** **Plain AcroForm** (no XFA), **Encrypted** with owner restrictions (`modifyDenied: true`, `annotateDenied: true`, form filling allowed), `96.2%` human-readable field names — measured in the [JustFill 134-Form Study](https://justfill.app/research/are-government-forms-fillable)

## Column-to-AcroForm Mapping

Unlike IRS forms, TxDMV's official Form 130-U uses descriptive AcroForm names (with spaces preserved):

| CSV Header | Official Form 130-U AcroForm Name | Notes |
| ---------- | --------------------------------- | ----- |
| `vin` | `1 Vehicle Identification Number` | 17-character VIN (synthetic `1TEST00000A00000x` in sample CSV) |
| `year` | `2 Year` | 4-digit year |
| `make` | `3 Make` | Uppercase standard |
| `body_style` | `4 Body Style` | 2-letter TxDMV code (`PK`, `4D`, `LL`, `UT`, `VN`) |
| `model` | `5 Model` | Vehicle model |
| `major_color` | `6 Major Color` | Primary color |
| `odometer_reading` | `9 Odometer Reading no tenths` | Whole miles only (no decimal tenths) |
| `empty_weight_lbs` | `11 Empty Weight` | Pounds (commercial / trailer deals) |
| `applicant_name` | `16 Applicant First Name or Entity Name Middle Name Last Name Suffix if any` | Individual or business entity |
| `applicant_address` + `applicant_city` + `applicant_state` + `applicant_zip` | `18 Applicant Mailing Address City State Zip` | Concatenate into Box 18 |
| `county_of_residence` | `19 Applicant County of Residence` | Texas county name |
| `previous_owner_name` | `20 Previous Owner Name or Entity Name City State` | Selling dealer or prior owner |
| `dealer_gdn` | Box 21 Dealer GDN | Constant per dealership rooftop |
| `sales_price`, `trade_in_allowance` | Box 38 Motor Vehicle Tax Statement | Verify statutory tax calculation with county tax office / webDEALER |
| `lienholder_name`, `first_lien_date` | `34 First Lienholder Name if any Mailing Address City State Zip`, `33 First Lien Date if any` | Blank date when cash sale (`NONE`) |

## Known Implementation Pitfalls

1. **Owner Encryption Flags (`modifyDenied` & `annotateDenied`):** `Form-130-U.pdf` is encrypted with an empty user password and permission bits denying page modification and annotations while allowing form fill. Libraries like `pdf-lib` require `{ ignoreEncryption: true }` when reading, and flattening/editing tools must handle encrypted streams gracefully.
2. **Signature Widgets (`3` fields):** Official Form 130-U includes 3 digital `/Sig` fields that do not accept spreadsheet text; skip `/Sig` fields when generating spreadsheet templates.
3. **Companion Dealer Packet Forms:** Auto, RV, and trailer dealerships typically reuse the exact same DMS CSV columns across **Form 130-U**, **VTR-130-SOF** (Texas Statement of Fact), and **VTR-141** (Trailer Verification Statement of Fact).

## Tools

- Inspect all 106 fields and encryption flags of `Form-130-U.pdf` locally: [JustFill PDF Form Field Inspector](https://justfill.app/pdf-form-fields)
- Batch-fill Form 130-U from DMS Excel/CSV: [JustFill Excel-to-PDF Batch Fill](https://justfill.app/solutions/fill-pdf-from-excel)
