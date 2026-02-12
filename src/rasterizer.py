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
    ) -> list:
        """
        Convert a PDF file to high-resolution images (handles multi-page PDFs).

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save the images
            image_format: Output format ('png' or 'jpeg')

        Returns:
            List of paths to the generated image files (one per page)
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Convert PDF to images (handles both single and multi-page documents)
        images = convert_from_path(
            pdf_path,
            dpi=self.dpi,
            fmt=image_format
        )

        if not images:
            raise ValueError(f"No images generated from PDF: {pdf_path}")

        # Generate output paths for all pages
        pdf_filename = Path(pdf_path).stem
        output_paths = []

        for page_num, image in enumerate(images, start=1):
            # For single-page documents, use simple naming; for multi-page, add page number
            if len(images) == 1:
                output_path = os.path.join(output_dir, f"{pdf_filename}.{image_format}")
            else:
                output_path = os.path.join(output_dir, f"{pdf_filename}_page{page_num}.{image_format}")

            # Save the image
            image.save(output_path, image_format.upper())
            output_paths.append(output_path)

        return output_paths

    def batch_convert(self, pdf_dir="output/pdfs", output_dir="output/images_clean"):
        """
        Convert all PDFs in a directory to images.

        Args:
            pdf_dir: Directory containing PDF files
            output_dir: Directory to save images

        Returns:
            List of generated image paths (flattened, includes all pages from all PDFs)
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
                img_paths = self.pdf_to_image(str(pdf_file), output_dir)
                image_paths.extend(img_paths)  # Flatten the list of paths
                if len(img_paths) == 1:
                    print(f"Converted: {pdf_file.name} -> {Path(img_paths[0]).name}")
                else:
                    print(f"Converted: {pdf_file.name} -> {len(img_paths)} pages")
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
