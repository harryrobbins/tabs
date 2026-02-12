from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


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


class ReceiptItem(BaseModel):
    """Represents a single item on a receipt."""
    description: str
    quantity: float
    unit_price: float
    total: float


class ReceiptData(BaseModel):
    """Complete receipt data structure - the ground truth for retail receipt generation."""
    id: str = Field(..., description="Unique ID for file naming")
    receipt_number: str
    transaction_id: str
    datetime: datetime
    store_name: str
    store_address: str
    store_phone: Optional[str] = None
    items: List[ReceiptItem]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total: float
    payment_method: str
    card_last_four: Optional[str] = None
    currency: str = "GBP"
    template_used: str = Field(default="", description="Name of template used for rendering")
