from pydantic import BaseModel, Field
from typing import List
from datetime import date


class LineItem(BaseModel):
    """Represents a single line item in an invoice."""
    description: str
    quantity: float
    unit_price: float
    total: float


class InvoiceData(BaseModel):
    """Complete invoice data structure - the ground truth for synthetic generation."""
    id: str = Field(..., description="Unique ID for file naming")
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
    currency: str = "GBP"
    template_used: str = Field(default="", description="Name of template used for rendering")
