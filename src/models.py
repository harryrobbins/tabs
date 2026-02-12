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


class Transaction(BaseModel):
    """Represents a single transaction on a bank statement."""
    date: date
    description: str
    debit: Optional[float] = None  # Money out
    credit: Optional[float] = None  # Money in
    balance: float


class BankStatementData(BaseModel):
    """Complete bank statement data structure - the ground truth for bank statement generation."""
    id: str = Field(..., description="Unique ID for file naming")
    account_holder_name: str
    account_holder_address: str
    account_number: str  # Last 4 digits
    sort_code: str  # Format: XX-XX-XX
    statement_period_start: date
    statement_period_end: date
    statement_date: date
    opening_balance: float
    closing_balance: float
    transactions: List[Transaction]
    bank_name: str
    bank_address: str
    currency: str = "GBP"
    template_used: str = Field(default="", description="Name of template used for rendering")
