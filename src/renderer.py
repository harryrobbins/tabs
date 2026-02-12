import os
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from src.models import InvoiceData, ReceiptData
from typing import Union


class Renderer:
    """Renders invoice and receipt data into PDFs using HTML/CSS templates."""

    def __init__(self, document_type="invoice"):
        """
        Initialize the renderer for a specific document type.

        Args:
            document_type: Type of document - 'invoice' or 'receipt'
        """
        self.document_type = document_type

        if document_type == "invoice":
            self.template_dir = "templates/invoices"
        elif document_type == "receipt":
            self.template_dir = "templates/receipts"
        else:
            raise ValueError(f"Unknown document type: {document_type}")

        self.env = Environment(loader=FileSystemLoader(self.template_dir))

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
        data: Union[InvoiceData, ReceiptData],
        output_dir="output/pdfs",
        template_name=None
    ) -> str:
        """
        Render invoice or receipt data to a PDF file.

        Args:
            data: InvoiceData or ReceiptData object to render
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

        # Use different variable names for invoices vs receipts in templates
        if self.document_type == "invoice":
            html_string = template.render(inv=data)
        else:  # receipt
            html_string = template.render(rec=data)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate output path
        output_path = os.path.join(output_dir, f"{data.id}.pdf")

        # Convert HTML to PDF
        HTML(string=html_string).write_pdf(output_path)

        return output_path


# Quick test if run directly
if __name__ == "__main__":
    from src.fabricator import DataFabricator, ReceiptFabricator

    print("Testing Invoice Renderer...")
    inv_fab = DataFabricator()
    inv_renderer = Renderer(document_type="invoice")

    invoice = inv_fab.generate_invoice()
    print(f"Generated invoice: {invoice.invoice_number}")

    pdf_path = inv_renderer.render_to_pdf(invoice)
    print(f"PDF created at: {pdf_path}")
    print(f"Template used: {invoice.template_used}")

    print("\n" + "="*70 + "\n")

    print("Testing Receipt Renderer...")
    rec_fab = ReceiptFabricator()
    rec_renderer = Renderer(document_type="receipt")

    receipt = rec_fab.generate_receipt()
    print(f"Generated receipt: {receipt.receipt_number}")

    pdf_path = rec_renderer.render_to_pdf(receipt)
    print(f"PDF created at: {pdf_path}")
    print(f"Template used: {receipt.template_used}")
