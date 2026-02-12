#!/usr/bin/env python3
"""
Artifact Engine - Synthetic Document Generator

Generates synthetic invoices and receipts with realistic degradation for OCR/LLM training.
Complete pipeline: Fabrication → Rendering → Rasterization → Entropy → Export
"""

import argparse
import time
from pathlib import Path

from src.fabricator import DataFabricator, ReceiptFabricator
from src.renderer import Renderer
from src.rasterizer import Rasterizer
from src.entropy import EntropyEngine
from src.exporter import GroundTruthExporter


def generate_documents(
    invoice_count: int = 0,
    receipt_count: int = 0,
    output_dir: str = "output",
    degradation: str = "medium",
    dpi: int = 300,
    clean_images: bool = False
):
    """
    Generate batches of synthetic invoices and/or receipts.

    Args:
        invoice_count: Number of invoices to generate
        receipt_count: Number of receipts to generate
        output_dir: Base output directory
        degradation: Degradation intensity ('light', 'medium', 'heavy')
        dpi: Image resolution for rasterization
        clean_images: Whether to save clean (pre-degradation) images
    """
    if invoice_count == 0 and receipt_count == 0:
        print("Error: Must specify at least one of --invoices or --receipts")
        return

    print("=" * 70)
    print("ARTIFACT ENGINE - Synthetic Document Generator")
    print("=" * 70)
    print(f"\nConfiguration:")
    if invoice_count > 0:
        print(f"  Invoices: {invoice_count}")
    if receipt_count > 0:
        print(f"  Receipts: {receipt_count}")
    print(f"  Output directory: {output_dir}")
    print(f"  Degradation level: {degradation}")
    print(f"  Image DPI: {dpi}")
    print(f"  Save clean images: {clean_images}")
    print()

    total_start = time.time()

    # Initialize shared components
    rasterizer = Rasterizer(dpi=dpi)
    entropy = EntropyEngine(intensity=degradation)
    exporter = GroundTruthExporter()

    # Process invoices
    if invoice_count > 0:
        print("\n" + "="*70)
        print("PROCESSING INVOICES")
        print("="*70 + "\n")

        invoices = process_document_type(
            document_type="invoice",
            count=invoice_count,
            output_dir=output_dir,
            rasterizer=rasterizer,
            entropy=entropy,
            clean_images=clean_images
        )

        # Export invoice ground truth
        print("[5/5] EXPORT - Creating invoice ground truth...")
        start_time = time.time()
        inv_gt_path = exporter.export_to_xlsx(invoices, f"{output_dir}/invoices_ground_truth.xlsx")
        inv_summary_path = exporter.export_summary(invoices, f"{output_dir}/invoices_summary.xlsx")
        export_time = time.time() - start_time
        print(f"  ✓ Ground truth: {inv_gt_path}")
        print(f"  ✓ Summary: {inv_summary_path}")
        print(f"  ✓ Completed in {export_time:.2f}s\n")

    # Process receipts
    if receipt_count > 0:
        print("\n" + "="*70)
        print("PROCESSING RECEIPTS")
        print("="*70 + "\n")

        receipts = process_document_type(
            document_type="receipt",
            count=receipt_count,
            output_dir=output_dir,
            rasterizer=rasterizer,
            entropy=entropy,
            clean_images=clean_images
        )

        # Export receipt ground truth
        print("[5/5] EXPORT - Creating receipt ground truth...")
        start_time = time.time()
        rec_gt_path = exporter.export_receipts_to_xlsx(receipts, f"{output_dir}/receipts_ground_truth.xlsx")
        rec_summary_path = exporter.export_receipts_summary(receipts, f"{output_dir}/receipts_summary.xlsx")
        export_time = time.time() - start_time
        print(f"  ✓ Ground truth: {rec_gt_path}")
        print(f"  ✓ Summary: {rec_summary_path}")
        print(f"  ✓ Completed in {export_time:.2f}s\n")

    # Final summary
    total_time = time.time() - total_start
    total_docs = invoice_count + receipt_count

    print("=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nTotal time: {total_time:.2f}s ({total_time/total_docs:.2f}s per document)")
    print(f"\nOutput structure:")
    print(f"  {output_dir}/")
    if invoice_count > 0:
        print(f"    ├── invoices_pdfs/              ({invoice_count} files)")
        if clean_images:
            print(f"    ├── invoices_images_clean/      ({invoice_count} files)")
        print(f"    ├── invoices_images_degraded/   ({invoice_count} files)")
        print(f"    ├── invoices_ground_truth.xlsx")
        print(f"    └── invoices_summary.xlsx")
    if receipt_count > 0:
        print(f"    ├── receipts_pdfs/              ({receipt_count} files)")
        if clean_images:
            print(f"    ├── receipts_images_clean/      ({receipt_count} files)")
        print(f"    ├── receipts_images_degraded/   ({receipt_count} files)")
        print(f"    ├── receipts_ground_truth.xlsx")
        print(f"    └── receipts_summary.xlsx")
    print()


def process_document_type(
    document_type: str,
    count: int,
    output_dir: str,
    rasterizer: Rasterizer,
    entropy: EntropyEngine,
    clean_images: bool
):
    """
    Process a single document type through the entire pipeline.

    Args:
        document_type: 'invoice' or 'receipt'
        count: Number of documents to generate
        output_dir: Base output directory
        rasterizer: Rasterizer instance
        entropy: EntropyEngine instance
        clean_images: Whether to keep clean images

    Returns:
        List of generated document data objects
    """
    # Setup output directories
    prefix = f"{document_type}s"
    pdf_dir = f"{output_dir}/{prefix}_pdfs"
    clean_dir = f"{output_dir}/{prefix}_images_clean"
    degraded_dir = f"{output_dir}/{prefix}_images_degraded"

    Path(pdf_dir).mkdir(parents=True, exist_ok=True)
    Path(clean_dir).mkdir(parents=True, exist_ok=True)
    Path(degraded_dir).mkdir(parents=True, exist_ok=True)

    # Initialize fabricator and renderer
    if document_type == "invoice":
        fabricator = DataFabricator()
        renderer = Renderer(document_type="invoice")
    else:  # receipt
        fabricator = ReceiptFabricator()
        renderer = Renderer(document_type="receipt")

    # Stage 1: Fabrication
    print(f"[1/4] FABRICATION - Generating synthetic {document_type} data...")
    start_time = time.time()

    documents = []
    for i in range(count):
        if document_type == "invoice":
            doc = fabricator.generate_invoice()
        else:
            doc = fabricator.generate_receipt()
        documents.append(doc)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Generated {i + 1}/{count} {prefix}")

    fab_time = time.time() - start_time
    print(f"  ✓ Completed in {fab_time:.2f}s\n")

    # Stage 2: Rendering
    print(f"[2/4] RENDERING - Converting data to PDFs...")
    start_time = time.time()

    pdf_paths = []
    for i, doc in enumerate(documents):
        pdf_path = renderer.render_to_pdf(doc, output_dir=pdf_dir)
        pdf_paths.append(pdf_path)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Rendered {i + 1}/{count} PDFs")

    render_time = time.time() - start_time
    print(f"  ✓ Completed in {render_time:.2f}s\n")

    # Stage 3: Rasterization
    print(f"[3/4] RASTERIZATION - Converting PDFs to images...")
    start_time = time.time()

    clean_paths = []
    for i, pdf_path in enumerate(pdf_paths):
        img_path = rasterizer.pdf_to_image(pdf_path, output_dir=clean_dir)
        clean_paths.append(img_path)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Converted {i + 1}/{count} images")

    raster_time = time.time() - start_time
    print(f"  ✓ Completed in {raster_time:.2f}s\n")

    # Stage 4: Entropy (Degradation)
    print(f"[4/4] ENTROPY - Applying degradation effects...")
    start_time = time.time()

    degraded_paths = []
    for i, clean_path in enumerate(clean_paths):
        deg_path = entropy.degrade_image(clean_path, output_dir=degraded_dir)
        degraded_paths.append(deg_path)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Degraded {i + 1}/{count} images")

    entropy_time = time.time() - start_time
    print(f"  ✓ Completed in {entropy_time:.2f}s\n")

    # Cleanup: Remove clean images if not requested
    if not clean_images:
        print("Cleaning up intermediate files...")
        for path in clean_paths:
            Path(path).unlink()
        print(f"  ✓ Removed {len(clean_paths)} clean images\n")

    return documents


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic invoice and receipt images for OCR/LLM training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 20 invoices
  python main.py --invoices 20

  # Generate 30 receipts
  python main.py --receipts 30

  # Generate both
  python main.py --invoices 20 --receipts 30

  # With heavy degradation and keep clean images
  python main.py --invoices 50 --receipts 50 --degradation heavy --keep-clean
        """
    )
    parser.add_argument(
        "--invoices",
        type=int,
        default=0,
        help="Number of invoices to generate (default: 0)"
    )
    parser.add_argument(
        "--receipts",
        type=int,
        default=0,
        help="Number of receipts to generate (default: 0)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output",
        help="Output directory (default: output)"
    )
    parser.add_argument(
        "-d", "--degradation",
        type=str,
        choices=["light", "medium", "heavy"],
        default="medium",
        help="Degradation intensity (default: medium)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Image resolution in DPI (default: 300)"
    )
    parser.add_argument(
        "--keep-clean",
        action="store_true",
        help="Keep clean (pre-degradation) images"
    )

    # Legacy support: -n maps to --invoices
    parser.add_argument(
        "-n",
        type=int,
        dest="legacy_count",
        help="(Legacy) Number of invoices - use --invoices instead"
    )

    args = parser.parse_args()

    # Handle legacy -n argument
    invoice_count = args.invoices
    if args.legacy_count is not None:
        if args.invoices == 0:
            invoice_count = args.legacy_count
            print(f"Warning: -n is deprecated, use --invoices instead\n")
        else:
            print(f"Warning: Both -n and --invoices specified, using --invoices\n")

    generate_documents(
        invoice_count=invoice_count,
        receipt_count=args.receipts,
        output_dir=args.output,
        degradation=args.degradation,
        dpi=args.dpi,
        clean_images=args.keep_clean
    )


if __name__ == "__main__":
    main()
