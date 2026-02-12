import pandas as pd
from pathlib import Path
from typing import List
from src.models import InvoiceData, ReceiptData


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

    def export_receipts_to_xlsx(
        self,
        receipts: List[ReceiptData],
        output_path="output/receipts_ground_truth.xlsx"
    ) -> str:
        """
        Export receipt data to an Excel file with denormalized structure.

        Args:
            receipts: List of ReceiptData objects
            output_path: Path to save the XLSX file

        Returns:
            Path to the created XLSX file
        """
        if not receipts:
            raise ValueError("No receipts to export")

        # Build denormalized rows
        rows = []
        for receipt in receipts:
            for idx, item in enumerate(receipt.items):
                row = {
                    # File reference
                    "image_id": receipt.id,
                    "image_filename": f"{receipt.id}.png",

                    # Receipt metadata
                    "receipt_number": receipt.receipt_number,
                    "transaction_id": receipt.transaction_id,
                    "datetime": receipt.datetime,
                    "template_used": receipt.template_used,

                    # Store information
                    "store_name": receipt.store_name,
                    "store_address": receipt.store_address,
                    "store_phone": receipt.store_phone,

                    # Item details
                    "item_index": idx,
                    "item_description": item.description,
                    "item_quantity": item.quantity,
                    "item_unit_price": item.unit_price,
                    "item_total": item.total,

                    # Receipt totals (repeated for each item)
                    "receipt_subtotal": receipt.subtotal,
                    "receipt_tax_rate": receipt.tax_rate,
                    "receipt_tax_amount": receipt.tax_amount,
                    "receipt_total": receipt.total,
                    "currency": receipt.currency,

                    # Payment information
                    "payment_method": receipt.payment_method,
                    "card_last_four": receipt.card_last_four,
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

    def export_receipts_summary(
        self,
        receipts: List[ReceiptData],
        output_path="output/receipts_summary.xlsx"
    ) -> str:
        """
        Export a summary view of receipts with one row per receipt.

        Args:
            receipts: List of ReceiptData objects
            output_path: Path to save the XLSX file

        Returns:
            Path to the created XLSX file
        """
        if not receipts:
            raise ValueError("No receipts to export")

        rows = []
        for receipt in receipts:
            row = {
                "image_id": receipt.id,
                "receipt_number": receipt.receipt_number,
                "transaction_id": receipt.transaction_id,
                "datetime": receipt.datetime,
                "store_name": receipt.store_name,
                "template": receipt.template_used,
                "num_items": len(receipt.items),
                "subtotal": receipt.subtotal,
                "tax_rate": receipt.tax_rate,
                "tax_amount": receipt.tax_amount,
                "total": receipt.total,
                "currency": receipt.currency,
                "payment_method": receipt.payment_method,
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
    from src.fabricator import DataFabricator, ReceiptFabricator

    print("Testing Invoice Exporter...")
    inv_fab = DataFabricator()
    invoices = [inv_fab.generate_invoice() for _ in range(5)]
    print(f"Generated {len(invoices)} test invoices")

    exporter = GroundTruthExporter()
    gt_path = exporter.export_to_xlsx(invoices, "output/test_invoices_ground_truth.xlsx")
    summary_path = exporter.export_summary(invoices, "output/test_invoices_summary.xlsx")

    print(f"Invoice ground truth exported to: {gt_path}")
    print(f"Invoice summary exported to: {summary_path}")

    print("\n" + "="*70 + "\n")

    print("Testing Receipt Exporter...")
    rec_fab = ReceiptFabricator()
    receipts = [rec_fab.generate_receipt() for _ in range(5)]
    print(f"Generated {len(receipts)} test receipts")

    gt_path = exporter.export_receipts_to_xlsx(receipts, "output/test_receipts_ground_truth.xlsx")
    summary_path = exporter.export_receipts_summary(receipts, "output/test_receipts_summary.xlsx")

    print(f"Receipt ground truth exported to: {gt_path}")
    print(f"Receipt summary exported to: {summary_path}")
