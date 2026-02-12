#!/usr/bin/env python3
"""
Artifact Engine - Synthetic Invoice Data Generator

This is the main orchestrator that runs the complete pipeline:
1. Fabricate synthetic invoice data
2. Render data into PDFs using templates
3. Rasterize PDFs to clean images
4. Apply degradation effects (entropy)
5. Export ground truth to XLSX
"""

import argparse
import time
from pathlib import Path

from src.fabricator import DataFabricator
from src.renderer import Renderer
from src.rasterizer import Rasterizer
from src.entropy import EntropyEngine
from src.exporter import GroundTruthExporter


def generate_batch(
    count: int = 20,
    output_dir: str = "output",
    degradation: str = "medium",
    dpi: int = 300,
    clean_images: bool = True
):
    """
    Generate a batch of synthetic invoice images with ground truth.

    Args:
        count: Number of invoices to generate
        output_dir: Base output directory
        degradation: Degradation intensity ('light', 'medium', 'heavy')
        dpi: Image resolution for rasterization
        clean_images: Whether to save clean (pre-degradation) images

    Returns:
        Dictionary with paths to generated files
    """
    print("=" * 70)
    print("ARTIFACT ENGINE - Synthetic Invoice Generator")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Invoice count: {count}")
    print(f"  Output directory: {output_dir}")
    print(f"  Degradation level: {degradation}")
    print(f"  Image DPI: {dpi}")
    print(f"  Save clean images: {clean_images}")
    print()

    # Setup output directories
    pdf_dir = f"{output_dir}/pdfs"
    clean_dir = f"{output_dir}/images_clean"
    degraded_dir = f"{output_dir}/images_degraded"

    Path(pdf_dir).mkdir(parents=True, exist_ok=True)
    Path(clean_dir).mkdir(parents=True, exist_ok=True)
    Path(degraded_dir).mkdir(parents=True, exist_ok=True)

    # Initialize components
    fabricator = DataFabricator()
    renderer = Renderer()
    rasterizer = Rasterizer(dpi=dpi)
    entropy = EntropyEngine(intensity=degradation)
    exporter = GroundTruthExporter()

    # Stage 1: Fabrication
    print("[1/5] FABRICATION - Generating synthetic invoice data...")
    start_time = time.time()

    invoices = []
    for i in range(count):
        invoice = fabricator.generate_invoice()
        invoices.append(invoice)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Generated {i + 1}/{count} invoices")

    fab_time = time.time() - start_time
    print(f"  ✓ Completed in {fab_time:.2f}s\n")

    # Stage 2: Rendering
    print("[2/5] RENDERING - Converting data to PDFs...")
    start_time = time.time()

    pdf_paths = []
    for i, invoice in enumerate(invoices):
        pdf_path = renderer.render_to_pdf(invoice, output_dir=pdf_dir)
        pdf_paths.append(pdf_path)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Rendered {i + 1}/{count} PDFs")

    render_time = time.time() - start_time
    print(f"  ✓ Completed in {render_time:.2f}s\n")

    # Stage 3: Rasterization
    print("[3/5] RASTERIZATION - Converting PDFs to images...")
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
    print("[4/5] ENTROPY - Applying degradation effects...")
    start_time = time.time()

    degraded_paths = []
    for i, clean_path in enumerate(clean_paths):
        deg_path = entropy.degrade_image(clean_path, output_dir=degraded_dir)
        degraded_paths.append(deg_path)
        if (i + 1) % 10 == 0 or (i + 1) == count:
            print(f"  Degraded {i + 1}/{count} images")

    entropy_time = time.time() - start_time
    print(f"  ✓ Completed in {entropy_time:.2f}s\n")

    # Stage 5: Export Ground Truth
    print("[5/5] EXPORT - Creating ground truth XLSX...")
    start_time = time.time()

    gt_path = exporter.export_to_xlsx(invoices, f"{output_dir}/ground_truth.xlsx")
    summary_path = exporter.export_summary(invoices, f"{output_dir}/summary.xlsx")

    export_time = time.time() - start_time
    print(f"  ✓ Ground truth: {gt_path}")
    print(f"  ✓ Summary: {summary_path}")
    print(f"  ✓ Completed in {export_time:.2f}s\n")

    # Cleanup: Remove clean images if not requested
    if not clean_images:
        print("Cleaning up intermediate files...")
        for path in clean_paths:
            Path(path).unlink()
        print(f"  ✓ Removed {len(clean_paths)} clean images\n")

    # Summary
    total_time = fab_time + render_time + raster_time + entropy_time + export_time
    print("=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nTotal time: {total_time:.2f}s ({total_time/count:.2f}s per invoice)")
    print(f"\nOutput structure:")
    print(f"  {output_dir}/")
    print(f"    ├── pdfs/              ({count} files)")
    if clean_images:
        print(f"    ├── images_clean/      ({count} files)")
    print(f"    ├── images_degraded/   ({count} files)")
    print(f"    ├── ground_truth.xlsx  (denormalized data)")
    print(f"    └── summary.xlsx       (invoice summary)")
    print()

    return {
        "invoices": invoices,
        "pdfs": pdf_paths,
        "clean_images": clean_paths if clean_images else [],
        "degraded_images": degraded_paths,
        "ground_truth": gt_path,
        "summary": summary_path,
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic invoice images for OCR/LLM training"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=20,
        help="Number of invoices to generate (default: 20)"
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

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output_dir=args.output,
        degradation=args.degradation,
        dpi=args.dpi,
        clean_images=args.keep_clean
    )


if __name__ == "__main__":
    main()
