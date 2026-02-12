import pandas as pd
from pathlib import Path
from typing import List
from src.models import InvoiceData


class GroundTruthExporter:
    """Exports invoice data to XLSX format as ground truth for validation."""

    def __init__(self):
        """Initialize the exporter."""
        pass

    def export_to_xlsx(
        self,
        invoices: List[InvoiceData],
        output_path="output/ground_truth.xlsx"
    ) -> str:
        """
        Export invoice data to an Excel file with denormalized structure.

        The output contains one row per line item, with invoice-level
        metadata repeated for each row. This denormalized structure
        makes it easier to validate extraction results.

        Args:
            invoices: List of InvoiceData objects
            output_path: Path to save the XLSX file

        Returns:
            Path to the created XLSX file
        """
        if not invoices:
            raise ValueError("No invoices to export")

        # Build denormalized rows
        rows = []
        for invoice in invoices:
            for idx, item in enumerate(invoice.line_items):
                row = {
                    # File reference
                    "image_id": invoice.id,
                    "image_filename": f"{invoice.id}.png",

                    # Invoice metadata
                    "invoice_number": invoice.invoice_number,
                    "invoice_date": invoice.date,
                    "due_date": invoice.due_date,
                    "template_used": invoice.template_used,

                    # Parties
                    "sender_name": invoice.sender_name,
                    "sender_address": invoice.sender_address,
                    "recipient_name": invoice.recipient_name,
                    "recipient_address": invoice.recipient_address,

                    # Line item details
                    "line_item_index": idx,
                    "item_description": item.description,
                    "item_quantity": item.quantity,
                    "item_unit_price": item.unit_price,
                    "item_total": item.total,

                    # Invoice totals (repeated for each line item)
                    "invoice_subtotal": invoice.subtotal,
                    "invoice_tax_rate": invoice.tax_rate,
                    "invoice_tax_amount": invoice.tax_amount,
                    "invoice_total": invoice.total,
                    "currency": invoice.currency,
                }
                rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(rows)

        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # Export to Excel
        df.to_excel(output_path, index=False, engine='openpyxl')

        return output_path

    def export_summary(
        self,
        invoices: List[InvoiceData],
        output_path="output/invoice_summary.xlsx"
    ) -> str:
        """
        Export a summary view with one row per invoice (no line items).

        Useful for quick overview of generated invoices.

        Args:
            invoices: List of InvoiceData objects
            output_path: Path to save the XLSX file

        Returns:
            Path to the created XLSX file
        """
        if not invoices:
            raise ValueError("No invoices to export")

        rows = []
        for invoice in invoices:
            row = {
                "image_id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "date": invoice.date,
                "due_date": invoice.due_date,
                "sender": invoice.sender_name,
                "recipient": invoice.recipient_name,
                "template": invoice.template_used,
                "num_line_items": len(invoice.line_items),
                "subtotal": invoice.subtotal,
                "tax_rate": invoice.tax_rate,
                "tax_amount": invoice.tax_amount,
                "total": invoice.total,
                "currency": invoice.currency,
            }
            rows.append(row)

        df = pd.DataFrame(rows)

        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        df.to_excel(output_path, index=False, engine='openpyxl')

        return output_path


# Quick test if run directly
if __name__ == "__main__":
    from src.fabricator import DataFabricator

    print("Testing exporter...")
    fab = DataFabricator()

    # Generate test invoices
    invoices = [fab.generate_invoice() for _ in range(5)]
    print(f"Generated {len(invoices)} test invoices")

    # Export to XLSX
    exporter = GroundTruthExporter()
    gt_path = exporter.export_to_xlsx(invoices, "output/test_ground_truth.xlsx")
    summary_path = exporter.export_summary(invoices, "output/test_summary.xlsx")

    print(f"Ground truth exported to: {gt_path}")
    print(f"Summary exported to: {summary_path}")
