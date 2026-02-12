# Artifact Engine

A synthetic data generation pipeline for creating realistic invoice, receipt, and bank statement images to test and train OCR/LLM document extraction systems.

## Overview

The Artifact Engine generates high-fidelity synthetic financial documents with a "Ground Truth First" approach: structured data is generated first, then rendered into visual documents (PDFs), converted to images, and finally degraded to simulate real-world scanning artifacts. Every pixel in the generated images is backed by known, structured data for exact precision/recall scoring of extraction tools.

## Features

- 📄 **Three Document Types** - Invoices, receipts, and bank statements with independent data
- 🎨 **25 Distinct Visual Templates** - 13 invoice, 10 receipt, and 2 bank statement templates
- 🇬🇧 **UK Localization** - British addresses, GBP currency, UK VAT rates, UK sort codes
- 📊 **Ground Truth Export** - Complete XLSX files mapping images to source data
- 🔄 **4-Stage Pipeline** - Fabrication → Rendering → Rasterization → Entropy
- 📑 **Multi-Page Support** - Bank statements with 10-300 transactions span multiple pages
- 🎲 **Realistic Degradation** - Rotation, noise, ink bleed, dirty rollers, JPEG compression
- ⚙️ **Configurable DPI** - Adjust image resolution from 72 to 600+ DPI
- ⚡ **Fast Generation** - ~2-3 seconds per document
- 🎯 **Mathematically Accurate** - All calculations are precise for validation testing

## Installation

### Prerequisites

- Python 3.12+
- `uv` package manager ([installation guide](https://docs.astral.sh/uv/))
- System dependencies for PDF rendering (poppler-utils)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd artifact-engine

# Install dependencies with uv
uv sync

# Run the generator
python main.py --invoices 20
```

## Quick Start

### Generate 20 invoices with default settings:
```bash
python main.py --invoices 20
```

### Generate 30 receipts with heavy degradation:
```bash
python main.py --receipts 30 --degradation heavy
```

### Generate 10 bank statements (multi-page):
```bash
python main.py --bank-statements 10
```

### Generate all document types:
```bash
python main.py --invoices 50 --receipts 100 --bank-statements 20
```

### High-resolution output with clean images preserved:
```bash
python main.py --invoices 20 --dpi 600 --keep-clean
```

### Low-resolution for faster testing:
```bash
python main.py --receipts 50 --dpi 150 --degradation light
```

### Custom output directory:
```bash
python main.py --invoices 100 -o my_dataset --degradation medium
```

## CLI Options

```
--invoices              Number of invoices to generate (default: 0)
--receipts              Number of receipts to generate (default: 0)
--bank-statements       Number of bank statements to generate (default: 0)
-o, --output           Output directory (default: output)
-d, --degradation      Degradation intensity: light, medium, heavy (default: medium)
--dpi                  Image resolution in DPI (default: 300)
--keep-clean           Keep clean (pre-degradation) images
```

**Note**: At least one document type must be specified (--invoices, --receipts, or --bank-statements).

**Legacy**: `-n` flag maps to `--invoices` for backwards compatibility but is deprecated.

## Pipeline Architecture

The system follows a **4-stage pipeline**:

### 1. Fabrication
Generates synthetic document data using Faker with mathematically correct calculations.

**Invoices:**
- UK company addresses and names
- 1-8 line items (services and products)
- Realistic date ranges (issue date, due date)
- UK VAT rates (0%, 5%, 20%)

**Receipts:**
- 5 store types: cafe, restaurant, supermarket, pharmacy, petrol
- 1-12 items with realistic pricing
- Payment methods: card (with last 4 digits) or cash
- Transaction timestamps

**Bank Statements:**
- UK bank names and addresses
- Sort codes (XX-XX-XX format) and account numbers
- 10-300 transactions per statement (creates multi-page PDFs)
- Realistic transaction types: salary, direct debits, card purchases, ATM withdrawals, transfers
- Running balance calculations

### 2. Rendering
Converts data into PDFs using Jinja2 HTML templates and WeasyPrint.
- Randomly selects from available templates per document type
- A4 page sizing
- Print-friendly CSS
- Multi-page support for long bank statements

### 3. Rasterization
Converts PDFs to high-resolution images using pdf2image.
- Configurable DPI (default 300)
- PNG format
- **Multi-page handling**: Bank statements with multiple pages are split into separate images
  - Single-page: `uuid.png`
  - Multi-page: `uuid_page1.png`, `uuid_page2.png`, etc.

### 4. Entropy
Applies 2D degradation effects using Augraphy:
- Rotation and skew
- Noise and speckling
- Ink bleeding
- Dirty rollers (scanner lines)
- JPEG compression artifacts
- Brightness/contrast variation

## Output Structure

```
output/
├── invoices_pdfs/                      # Invoice PDF files
├── invoices_images_clean/              # Clean images (if --keep-clean)
├── invoices_images_degraded/           # Final degraded invoice images
├── invoices_ground_truth.xlsx          # Denormalized invoice ground truth
├── invoices_summary.xlsx               # Invoice-level summary
│
├── receipts_pdfs/                      # Receipt PDF files
├── receipts_images_clean/              # Clean images (if --keep-clean)
├── receipts_images_degraded/           # Final degraded receipt images
├── receipts_ground_truth.xlsx          # Denormalized receipt ground truth
├── receipts_summary.xlsx               # Receipt-level summary
│
├── bank_statements_pdfs/               # Bank statement PDF files
├── bank_statements_images_clean/       # Clean images (if --keep-clean)
├── bank_statements_images_degraded/    # Final degraded images (multi-page)
├── statements_ground_truth.xlsx        # Denormalized statement ground truth
└── statements_summary.xlsx             # Statement-level summary
```

## Document Templates

### Invoice Templates (13 total)

| Template | Style Description |
|----------|------------------|
| `classic` | Traditional bold headers, clean grid layout |
| `modern` | Minimal design, lots of whitespace, subtle colors |
| `corporate` | Professional gradient header, structured layout |
| `minimal` | Ultra-clean monospace, Courier font |
| `vibrant` | Bold gradients, colorful, eye-catching |
| `grid` | Heavy borders, boxed sections, very structured |
| `elegant` | Serif fonts, ornamental dividers, formal |
| `tech` | Startup aesthetic, rounded corners, modern |
| `simple` | Basic no-frills design with standard borders |
| `luxury` | Gold accents, premium styling, sophisticated |
| `retro` | Vintage 1970s style, typewriter aesthetic |
| `compact` | Information-dense, small fonts, efficient |
| `creative` | Playful gradients, emojis, unique layout |

### Receipt Templates (10 total)

| Template | Style Description |
|----------|------------------|
| `thermal` | Classic thermal printer style, monospace |
| `modern_receipt` | Clean modern layout with subtle colors |
| `minimal_receipt` | Ultra-minimal design, essential info only |
| `cafe_style` | Warm coffee shop aesthetic |
| `grocery` | Supermarket style with product codes |
| `compact_receipt` | Information-dense, space-efficient |
| `premium` | Upscale restaurant styling |
| `simple_receipt` | Basic clean design |
| `tech_receipt` | Modern tech-forward design |
| `classic_receipt` | Traditional receipt layout |

### Bank Statement Templates (2 total)

| Template | Style Description |
|----------|------------------|
| `with_pages` | Professional blue theme with page numbers ("Page X of Y") |
| `no_pages` | Modern gradient header without pagination |

Both templates support multi-page statements (10-300 transactions).

## Ground Truth Data

### Invoice Ground Truth
The `invoices_ground_truth.xlsx` file contains denormalized data with one row per line item:

- **File Reference**: `image_id`, `image_filename`
- **Invoice Metadata**: `invoice_number`, `invoice_date`, `due_date`, `template_used`
- **Parties**: `sender_name`, `sender_address`, `recipient_name`, `recipient_address`
- **Line Items**: `line_item_index`, `item_description`, `item_quantity`, `item_unit_price`, `item_total`
- **Totals**: `invoice_subtotal`, `invoice_tax_rate`, `invoice_tax_amount`, `invoice_total`, `currency`

### Receipt Ground Truth
The `receipts_ground_truth.xlsx` file contains denormalized data with one row per item:

- **File Reference**: `image_id`, `image_filename`
- **Receipt Metadata**: `receipt_number`, `transaction_id`, `datetime`, `template_used`
- **Store Info**: `store_name`, `store_address`, `store_phone`
- **Items**: `item_index`, `item_description`, `item_quantity`, `item_unit_price`, `item_total`
- **Totals**: `receipt_subtotal`, `receipt_tax_rate`, `receipt_tax_amount`, `receipt_total`, `currency`
- **Payment**: `payment_method`, `card_last_four`

### Bank Statement Ground Truth
The `statements_ground_truth.xlsx` file contains denormalized data with one row per transaction:

- **File Reference**: `image_id`, `image_filename`
- **Statement Metadata**: `statement_period_start`, `statement_period_end`, `statement_date`, `template_used`
- **Account Info**: `account_holder_name`, `account_holder_address`, `sort_code`, `account_number`
- **Bank Info**: `bank_name`, `bank_address`
- **Balances**: `opening_balance`, `closing_balance`, `num_transactions`
- **Transactions**: `transaction_index`, `transaction_date`, `transaction_description`, `transaction_debit`, `transaction_credit`, `transaction_balance`
- **Currency**: `currency`

## Project Structure

```
artifact-engine/
├── main.py                      # Main orchestrator and CLI
├── src/
│   ├── models.py               # Pydantic data models (InvoiceData, ReceiptData, BankStatementData)
│   ├── fabricator.py           # Synthetic data generation (3 fabricators)
│   ├── renderer.py             # HTML → PDF conversion
│   ├── rasterizer.py           # PDF → Image conversion (multi-page support)
│   ├── entropy.py              # Image degradation pipeline
│   └── exporter.py             # XLSX ground truth export (all document types)
├── templates/
│   ├── invoices/               # 13 HTML/CSS invoice templates
│   ├── receipts/               # 10 HTML/CSS receipt templates
│   └── bank_statements/        # 2 HTML/CSS bank statement templates
├── output/                     # Generated files (gitignored)
├── pyproject.toml              # Dependencies
├── CLAUDE.md                   # Claude Code guidance
└── README.md                   # This file
```

## Development

### Testing Individual Components

```bash
# Test invoice fabrication
python -m src.fabricator

# Test PDF rendering
python -m src.renderer

# Test image rasterization
python -m src.rasterizer

# Test entropy/degradation
python -m src.entropy

# Test XLSX export
python -m src.exporter
```

### Adding New Templates

**For Invoices:**
1. Create a new HTML file in `templates/invoices/`
2. Use Jinja2 syntax to inject data: `{{ inv.invoice_number }}`, `{{ inv.sender_name }}`, etc.
3. Loop through line items: `{% for item in inv.line_items %}`
4. Ensure A4 page sizing: `@page { size: A4; margin: 20mm; }`
5. Use UK formatting: £ symbol, VAT terminology
6. Test with: `python main.py --invoices 5`

**For Receipts:**
1. Create a new HTML file in `templates/receipts/`
2. Use Jinja2 syntax: `{{ rec.store_name }}`, `{{ rec.datetime }}`, etc.
3. Loop through items: `{% for item in rec.items %}`
4. Consider thermal printer aesthetic for realism
5. Test with: `python main.py --receipts 5`

**For Bank Statements:**
1. Create a new HTML file in `templates/bank_statements/`
2. Use Jinja2 syntax: `{{ stmt.bank_name }}`, `{{ stmt.account_number }}`, etc.
3. Loop through transactions: `{% for trans in stmt.transactions %}`
4. Add page numbering if desired: `@page { @bottom-center { content: "Page " counter(page); } }`
5. Test with: `python main.py --bank-statements 2`

## Key Design Principles

- **Ground Truth Integrity**: All monetary calculations are mathematically precise
- **Data First, Visuals Second**: Always generate and save structured data before rendering
- **Template Separation**: Visual templates are completely decoupled from data models
- **Multi-Page Support**: Long documents (bank statements) are properly split across pages
- **Independent Data**: Invoices, receipts, and bank statements have completely separate data
- **Reproducibility**: Deterministic output possible with seed parameters (future enhancement)

## Use Cases

- Training OCR/LLM models for financial document extraction
- Testing document processing pipelines across multiple document types
- Benchmarking extraction accuracy for invoices, receipts, and statements
- Generating demo/test datasets without privacy concerns
- Creating "hard examples" to challenge extraction models
- Testing multi-page document handling
- Evaluating DPI/resolution requirements for OCR systems

## Performance

- **Generation Speed**: ~2-3 seconds per single-page document
- **Bank Statements**: ~15-20 seconds per multi-page statement (varies with transaction count)
- **Batch Processing**: 100 single-page documents in ~5 minutes
- **Multi-Page**: 10 bank statements (50-100 pages total) in ~3 minutes
- **Scalability**: Tested with batches up to 1000 documents
- **DPI Impact**: 150 DPI ~2x faster than 300 DPI; 600 DPI ~2x slower than 300 DPI

## Requirements

Key dependencies:
- `faker` - Synthetic data generation with UK locale
- `jinja2` - HTML templating
- `weasyprint` - PDF rendering
- `pdf2image` - Multi-page PDF to image conversion
- `augraphy` - Document degradation effects
- `pandas` + `openpyxl` - XLSX ground truth export
- `pydantic` - Data validation and modeling

See `pyproject.toml` for complete dependency list.

## Multi-Page Document Handling

Bank statements with 10-300 transactions automatically generate multi-page PDFs. The rasterizer handles this intelligently:

- **Single-page documents** (invoices, receipts, short statements): `uuid.png`
- **Multi-page documents** (long bank statements): `uuid_page1.png`, `uuid_page2.png`, ..., `uuid_pageN.png`

Each page is:
1. Converted to a separate PNG image
2. Degraded independently with entropy effects
3. Tracked in the ground truth XLSX with the same document ID

This ensures OCR/LLM systems can be tested on both single-page and multi-page document scenarios.

## Known Limitations

- Bank statements currently use GBP only (£ symbol hardcoded in templates)
- Degradation effects are random (not reproducible without seed)
- Templates are UK-focused (addresses, sort codes, VAT terminology)
- No handwritten text or signatures
- No logos or company branding (future enhancement)

## Future Enhancements

- [ ] More templates (target: 20+ per document type)
- [ ] Logo generation/integration
- [ ] 3D degradation effects (page curl, perspective)
- [ ] Configurable degradation intensity per effect
- [ ] Seeded randomness for reproducibility
- [ ] Web UI for generation
- [ ] Hard example generation mode (worst-case degradation)
- [ ] Multi-currency support beyond GBP
- [ ] Handwritten annotations/signatures
- [ ] Additional document types (tax forms, purchase orders, delivery notes)

## License

[Add your license here]

## Acknowledgments

Built with [Augraphy](https://github.com/sparkfish/augraphy) for document degradation, [WeasyPrint](https://weasyprint.org/) for PDF rendering, and [Faker](https://faker.readthedocs.io/) for synthetic data generation.

---

**Version**: 1.0
**Last Updated**: 2026-02-12
