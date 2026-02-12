# Synthetic Invoice Data Generator - Implementation Plan

## Project Overview

**Goal:** Build a synthetic data generation pipeline that creates realistic invoice images for testing OCR/LLM extraction tools. The pipeline generates structured data first (ground truth), renders it into visual documents, converts to images, and applies realistic degradation effects.

**Core Principle:** Ground Truth First - every generated image is backed by known, structured data for exact validation of extraction accuracy.

## Tech Stack

- **Language:** Python 3.11+
- **Package Manager:** uv
- **Web Framework:** FastAPI (for triggering generation jobs)
- **LLM Integration:** litellm (optional, for creative text generation)
- **Data Generation:** Faker
- **Templating:** Jinja2 (HTML/CSS templates)
- **PDF Rendering:** WeasyPrint (HTML → PDF)
- **Image Conversion:** pdf2image (poppler wrapper)
- **Image Degradation:** Augraphy (specialized for document degradation)
- **Data Export:** pandas + openpyxl (XLSX output)
- **Data Models:** Pydantic

## Architecture: 4-Stage Pipeline

```
1. FABRICATION → 2. RENDERING → 3. RASTERIZATION → 4. ENTROPY
   (JSON data)     (PDF files)      (clean images)    (degraded images)
```

### Stage 1: Fabrication
- Generate structured invoice data using Faker
- Calculate mathematically correct totals
- Optional: Use litellm for realistic line item descriptions
- Output: List of `InvoiceData` Pydantic objects

### Stage 2: Rendering
- Load HTML/CSS Jinja2 templates
- Inject data into randomly selected template
- Convert to PDF using WeasyPrint
- Output: PDF files

### Stage 3: Rasterization
- Convert PDF pages to high-resolution images
- Output: Clean PNG/JPEG images

### Stage 4: Entropy
- Apply 2D degradation effects using Augraphy:
  - Rotation/skew
  - Noise/speckling
  - Blur
  - JPEG compression artifacts
  - Scanner lines
  - Paper texture
- Output: Realistic "scanned" images

## Data Models

```python
class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class InvoiceData(BaseModel):
    id: str                    # UUID for file naming
    invoice_number: str
    date: date
    due_date: date
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_address: str
    line_items: List[LineItem]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total: float
    currency: str = "USD"
```

## Project Structure

```
/var/web/tabs/
├── pyproject.toml          # uv dependencies
├── main.py                 # FastAPI entry point & orchestration
├── src/
│   ├── models.py           # Pydantic data models
│   ├── fabricator.py       # Data generation logic
│   ├── renderer.py         # HTML → PDF conversion
│   ├── rasterizer.py       # PDF → Image conversion
│   ├── entropy.py          # Image degradation pipeline
│   └── exporter.py         # XLSX ground truth export
├── templates/
│   └── invoices/
│       ├── template_01.html
│       ├── template_02.html
│       └── template_03.html
├── assets/
│   └── logos/              # Fake company logos (optional)
└── output/
    ├── pdfs/               # Clean PDFs
    ├── images_clean/       # Clean rasterized images
    ├── images_degraded/    # Final degraded images
    └── ground_truth.xlsx   # Master data file
```

## POC Implementation Steps

### Phase 1: Foundation (Core Pipeline)
1. **Initialize project**
   - Set up uv environment
   - Install dependencies
   - Create project structure

2. **Build data layer**
   - Create `models.py` with Pydantic schemas
   - Build `fabricator.py` to generate synthetic invoice data
   - Test: Generate 10 invoices and print JSON

3. **Create HTML templates**
   - Design 3 distinct invoice layouts in HTML/CSS
   - Use Jinja2 syntax for data injection
   - Ensure print-friendly styling (A4 page size)

4. **Implement renderer**
   - Build `renderer.py` with WeasyPrint integration
   - Test: Generate PDFs from synthetic data
   - Verify visual output quality

### Phase 2: Image Pipeline
5. **Build rasterizer**
   - Create `rasterizer.py` with pdf2image
   - Convert PDFs to high-res images (300 DPI)
   - Output clean images for comparison

6. **Implement entropy engine**
   - Build `entropy.py` with Augraphy pipeline
   - Configure 2D degradation effects:
     - Geometric: rotation (1-5°), skew
     - Noise: Gaussian noise, speckling
     - Quality: JPEG compression, blur
   - Test on sample images

### Phase 3: Orchestration & Export
7. **Build exporter**
   - Create `exporter.py` to generate XLSX
   - Denormalize invoice data into flat rows
   - Map image filenames to ground truth data

8. **Create main orchestrator**
   - Build `main.py` to run full pipeline
   - Add CLI arguments (count, output dir, etc.)
   - Optional: FastAPI endpoints for web triggering

9. **Generate POC batch**
   - Run pipeline to generate 50-100 invoices
   - Validate output structure
   - Verify image quality and degradation effects

## Success Criteria for POC

- [ ] Generate 50+ unique invoices with varied data
- [ ] 3 distinct visual templates working
- [ ] Clean and degraded image sets created
- [ ] ground_truth.xlsx contains complete data mapping
- [ ] Images have realistic degradation (rotation, noise, artifacts)
- [ ] All calculations in ground truth are mathematically correct
- [ ] Pipeline runs end-to-end without manual intervention

## Future Enhancements (Post-POC)

- Add more document types (bank statements, receipts)
- Expand template library (30+ invoice designs)
- Logo generation/integration
- 3D degradation effects (page curl, perspective)
- Configurable degradation intensity levels
- Batch processing API
- Template preview UI
- Hard example generation (intentionally challenging cases)

## Dependencies (pyproject.toml)

```toml
dependencies = [
    "fastapi",
    "uvicorn",
    "jinja2",
    "weasyprint",
    "faker",
    "pandas",
    "openpyxl",
    "litellm",
    "pdf2image",
    "augraphy",
    "opencv-python-headless",
    "pydantic"
]
```

## Notes

- **Ground truth integrity:** All monetary calculations must be precise (use Decimal if needed)
- **Template variety:** Focus on layout differences (grid vs. list, modern vs. classic)
- **Degradation realism:** Balance between challenging and readable
- **Performance:** Start with small batches (10-20) during development
- **Deterministic option:** Consider adding seed parameter for reproducible datasets
