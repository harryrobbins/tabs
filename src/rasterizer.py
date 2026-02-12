import os
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image


class Rasterizer:
    """Converts PDF files to high-resolution images."""

    def __init__(self, dpi=300):
        """
        Initialize the rasterizer.

        Args:
            dpi: Resolution for image conversion (default 300 for high quality)
        """
        self.dpi = dpi

    def pdf_to_image(
        self,
        pdf_path: str,
        output_dir="output/images_clean",
        image_format="png"
    ) -> str:
        """
        Convert a PDF file to a high-resolution image.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save the image
            image_format: Output format ('png' or 'jpeg')

        Returns:
            Path to the generated image file
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Convert PDF to images (assuming single-page invoices)
        images = convert_from_path(
            pdf_path,
            dpi=self.dpi,
            fmt=image_format
        )

        if not images:
            raise ValueError(f"No images generated from PDF: {pdf_path}")

        # For single-page documents, take the first page
        image = images[0]

        # Generate output path (preserve the same UUID from filename)
        pdf_filename = Path(pdf_path).stem
        output_path = os.path.join(output_dir, f"{pdf_filename}.{image_format}")

        # Save the image
        image.save(output_path, image_format.upper())

        return output_path

    def batch_convert(self, pdf_dir="output/pdfs", output_dir="output/images_clean"):
        """
        Convert all PDFs in a directory to images.

        Args:
            pdf_dir: Directory containing PDF files
            output_dir: Directory to save images

        Returns:
            List of generated image paths
        """
        pdf_path = Path(pdf_dir)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

        pdf_files = list(pdf_path.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in {pdf_dir}")
            return []

        image_paths = []
        for pdf_file in pdf_files:
            try:
                img_path = self.pdf_to_image(str(pdf_file), output_dir)
                image_paths.append(img_path)
                print(f"Converted: {pdf_file.name} -> {Path(img_path).name}")
            except Exception as e:
                print(f"Error converting {pdf_file.name}: {e}")

        return image_paths


# Quick test if run directly
if __name__ == "__main__":
    print("Testing rasterizer...")
    rasterizer = Rasterizer(dpi=300)

    # Convert existing PDFs
    images = rasterizer.batch_convert()
    print(f"\nConverted {len(images)} PDF(s) to images")

    if images:
        print(f"First image: {images[0]}")
