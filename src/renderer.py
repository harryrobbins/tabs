import os
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from src.models import InvoiceData


class Renderer:
    """Renders InvoiceData into PDFs using HTML/CSS templates."""

    def __init__(self, template_dir="templates/invoices"):
        """
        Initialize the renderer with a template directory.

        Args:
            template_dir: Path to directory containing Jinja2 templates
        """
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # Discover available templates
        self.templates = self._discover_templates()

    def _discover_templates(self):
        """Scan template directory for available HTML templates."""
        template_path = Path(self.template_dir)
        if not template_path.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")

        templates = list(template_path.glob("*.html"))
        if not templates:
            raise FileNotFoundError(f"No HTML templates found in {self.template_dir}")

        return [t.name for t in templates]

    def render_to_pdf(
        self,
        data: InvoiceData,
        output_dir="output/pdfs",
        template_name=None
    ) -> str:
        """
        Render invoice data to a PDF file.

        Args:
            data: InvoiceData object to render
            output_dir: Directory to save the PDF
            template_name: Specific template to use (if None, random selection)

        Returns:
            Path to the generated PDF file
        """
        # Select template
        if template_name is None:
            template_name = random.choice(self.templates)
        elif template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found. Available: {self.templates}")

        # Update the data object to track which template was used
        data.template_used = template_name.replace('.html', '')

        # Load and render template
        template = self.env.get_template(template_name)
        html_string = template.render(inv=data)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate output path
        output_path = os.path.join(output_dir, f"{data.id}.pdf")

        # Convert HTML to PDF
        HTML(string=html_string).write_pdf(output_path)

        return output_path


# Quick test if run directly
if __name__ == "__main__":
    from src.fabricator import DataFabricator

    print("Testing renderer...")
    fab = DataFabricator()
    renderer = Renderer()

    # Generate a test invoice
    invoice = fab.generate_invoice()
    print(f"Generated invoice: {invoice.invoice_number}")

    # Render it to PDF
    pdf_path = renderer.render_to_pdf(invoice)
    print(f"PDF created at: {pdf_path}")
    print(f"Template used: {invoice.template_used}")
