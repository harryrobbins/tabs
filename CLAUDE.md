# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **synthetic data generation pipeline** for creating realistic invoice images to test OCR/LLM extraction tools. The system operates on a "Ground Truth First" principle: structured data is generated first, then rendered into visual documents (PDFs), converted to images, and finally degraded to simulate real-world scanning artifacts.

See `IMPLEMENTATION_PLAN.md` for detailed architecture and implementation steps.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv
uv sync

# Run the main application
python main.py
```

Note: The project uses `uv` for package management (requires Python 3.12+).

## Pipeline Architecture

The system follows a **4-stage pipeline**:

1. **Fabrication** (`src/fabricator.py`) - Generates synthetic invoice data using Faker, with mathematically correct calculations
2. **Rendering** (`src/renderer.py`) - Converts data into PDFs using Jinja2 HTML templates + WeasyPrint
3. **Rasterization** (`src/rasterizer.py`) - Converts PDFs to high-res images using pdf2image
4. **Entropy** (`src/entropy.py`) - Applies 2D degradation effects (rotation, noise, blur, speckling) using Augraphy

All stages output to `/output/` with subdirectories for each stage. The final `ground_truth.xlsx` maps image filenames to their source data.

## Key Design Principles

- **Ground Truth Integrity**: All monetary calculations must be mathematically precise. The ground truth data is the source of truth for validating the extraction pipeline.
- **Data First, Visuals Second**: Always generate and save structured data before rendering. Never generate visuals without corresponding ground truth.
- **Template Separation**: Visual templates (HTML/CSS) are completely decoupled from data models. One dataset can render across multiple templates.
- **Reproducibility**: Consider using seed parameters for deterministic output when testing.

## Data Flow

```
InvoiceData (Pydantic) → HTML (Jinja2) → PDF (WeasyPrint) → Clean Image (pdf2image) → Degraded Image (Augraphy)
                      ↓
              ground_truth.xlsx (pandas/openpyxl)
```

## Important Notes

- The `InvoiceData` Pydantic model in `src/models.py` is the schema contract for the entire pipeline
- Templates in `templates/invoices/` must use A4 page sizing and print-friendly CSS
- Augraphy degradation effects are configured for 2D transforms only (rotation, skew, noise, compression)
- The exporter denormalizes relational data into flat rows for the XLSX output
