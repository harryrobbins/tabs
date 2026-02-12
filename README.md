# Artifact Engine

A synthetic data generation pipeline for creating realistic invoice images to test and train OCR/LLM document extraction systems.

## Overview

The Artifact Engine generates high-fidelity synthetic invoices with a "Ground Truth First" approach: structured data is generated first, then rendered into visual documents (PDFs), converted to images, and finally degraded to simulate real-world scanning artifacts. Every pixel in the generated images is backed by known, structured data for exact precision/recall scoring of extraction tools.

## Features

- 🎨 **13 Distinct Visual Templates** - From classic to modern, minimal to luxury, ensuring diverse training data
- 🇬🇧 **UK Localization** - British addresses, GBP currency, UK VAT rates
- 📊 **Ground Truth Export** - Complete XLSX files mapping images to source data
- 🔄 **4-Stage Pipeline** - Fabrication → Rendering → Rasterization → Entropy
- 🎲 **Realistic Degradation** - Rotation, noise, ink bleed, dirty rollers, JPEG compression
- ⚡ **Fast Generation** - ~3 seconds per invoice
- 🎯 **Mathematically Accurate** - All calculations are precise for validation testing

## Installation

### Prerequisites

- Python 3.12+
- `uv` package manager ([installation guide](https://docs.astral.sh/uv/))

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd artifact-engine

# Install dependencies with uv
uv sync

# Run the generator
python main.py -n 20
```

## Quick Start

### Generate 20 invoices with default settings:
```bash
python main.py -n 20
```

### Generate 50 invoices with heavy degradation:
```bash
python main.py -n 50 --degradation heavy
```

### Generate invoices and keep clean (pre-degradation) images:
```bash
python main.py -n 30 --keep-clean
```

### Custom output directory:
```bash
python main.py -n 100 -o my_output --degradation light
```

## CLI Options

```
-n, --count         Number of invoices to generate (default: 20)
-o, --output        Output directory (default: output)
-d, --degradation   Degradation intensity: light, medium, heavy (default: medium)
--dpi              Image resolution in DPI (default: 300)
--keep-clean       Keep clean (pre-degradation) images
```

## Pipeline Architecture

The system follows a **4-stage pipeline**:

### 1. Fabrication
Generates synthetic invoice data using Faker with mathematically correct calculations.
- UK addresses and company names
- Varied line items (services and products)
- Realistic date ranges
- UK VAT rates (0%, 5%, 20%)

### 2. Rendering
Converts data into PDFs using Jinja2 HTML templates and WeasyPrint.
- Randomly selects from 13 templates
- A4 page sizing
- Print-friendly CSS

### 3. Rasterization
Converts PDFs to high-resolution images using pdf2image.
- Default 300 DPI
- PNG format

### 4. Entropy
Applies 2D degradation effects using Augraphy:
- Rotation and skew
- Noise and speckling
- Ink bleeding
- Dirty rollers (scanner lines)
- JPEG compression artifacts

## Output Structure

```
output/
├── pdfs/                   # Clean PDF files
├── images_clean/           # Clean rasterized images (if --keep-clean)
├── images_degraded/        # Final degraded images
├── ground_truth.xlsx       # Denormalized ground truth data
└── summary.xlsx            # Invoice-level summary
```

## Invoice Templates

The generator includes 13 distinct visual styles:

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

## Ground Truth Data

The `ground_truth.xlsx` file contains denormalized data with one row per line item:

- **File Reference**: `image_id`, `image_filename`
- **Invoice Metadata**: `invoice_number`, `invoice_date`, `due_date`, `template_used`
- **Parties**: `sender_name`, `sender_address`, `recipient_name`, `recipient_address`
- **Line Items**: `item_description`, `item_quantity`, `item_unit_price`, `item_total`
- **Totals**: `invoice_subtotal`, `invoice_tax_rate`, `invoice_tax_amount`, `invoice_total`, `currency`

## Project Structure

```
artifact-engine/
├── main.py                 # Main orchestrator and CLI
├── src/
│   ├── models.py          # Pydantic data models
│   ├── fabricator.py      # Synthetic data generation
│   ├── renderer.py        # HTML → PDF conversion
│   ├── rasterizer.py      # PDF → Image conversion
│   ├── entropy.py         # Image degradation pipeline
│   └── exporter.py        # XLSX ground truth export
├── templates/
│   └── invoices/          # HTML/CSS invoice templates
├── assets/
│   └── logos/             # Company logos (optional)
├── output/                # Generated files (gitignored)
├── pyproject.toml         # Dependencies
├── CLAUDE.md              # Claude Code guidance
└── README.md              # This file
```

## Development

### Testing Individual Components

```bash
# Test data fabrication
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

1. Create a new HTML file in `templates/invoices/`
2. Use Jinja2 syntax to inject data: `{{ inv.invoice_number }}`
3. Ensure A4 page sizing: `@page { size: A4; margin: 20mm; }`
4. Use UK formatting: £ symbol, VAT terminology
5. Test with: `python main.py -n 5`

## Key Design Principles

- **Ground Truth Integrity**: All monetary calculations are mathematically precise
- **Data First, Visuals Second**: Always generate and save structured data before rendering
- **Template Separation**: Visual templates are completely decoupled from data models
- **Reproducibility**: Deterministic output possible with seed parameters

## Use Cases

- Training OCR/LLM models for invoice extraction
- Testing document processing pipelines
- Benchmarking extraction accuracy
- Generating demo/test datasets without privacy concerns
- Creating "hard examples" to challenge extraction models

## Performance

- **Generation Speed**: ~3 seconds per invoice (on standard hardware)
- **Batch Processing**: 100 invoices in ~5 minutes
- **Scalability**: Tested with batches up to 1000 invoices

## Requirements

Key dependencies:
- `faker` - Synthetic data generation
- `jinja2` - HTML templating
- `weasyprint` - PDF rendering
- `pdf2image` - Image conversion
- `augraphy` - Document degradation
- `pandas` + `openpyxl` - XLSX export
- `pydantic` - Data validation

See `pyproject.toml` for complete dependency list.

## Future Enhancements

- [ ] Additional document types (bank statements, receipts)
- [ ] More templates (target: 30+ for invoices)
- [ ] Logo generation/integration
- [ ] 3D degradation effects (page curl, perspective)
- [ ] Configurable degradation intensity per effect
- [ ] Web UI for generation
- [ ] Hard example generation mode
- [ ] Multi-page invoice support

## License

[Add your license here]

## Acknowledgments

Built with [Augraphy](https://github.com/sparkfish/augraphy) for document degradation and [WeasyPrint](https://weasyprint.org/) for PDF rendering.
