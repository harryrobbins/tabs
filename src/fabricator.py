import random
import uuid
from datetime import timedelta
from faker import Faker
from src.models import InvoiceData, LineItem

fake = Faker('en_GB')  # Use UK locale for British addresses and names


class DataFabricator:
    """Generates synthetic invoice data with mathematically correct calculations."""

    def __init__(self, use_llm=False):
        """
        Initialize the fabricator.

        Args:
            use_llm: Whether to use LiteLLM for creative text generation (not implemented yet)
        """
        self.use_llm = use_llm

        # Vocabularies for realistic but varied line items
        self.services = [
            "Consulting Services",
            "Web Development",
            "Database Optimization",
            "API Integration",
            "Cloud Hosting",
            "Security Audit",
            "UI/UX Design",
            "Maintenance Retainer",
            "Code Review",
            "Performance Testing",
            "Technical Documentation",
            "DevOps Support",
            "Data Migration",
            "Mobile App Development",
            "System Architecture",
        ]

        self.products = [
            "Software License",
            "Hardware Component",
            "Server Access",
            "Cloud Storage",
            "API Credits",
            "Premium Support",
            "Training Materials",
            "Documentation Package",
            "Development Tools",
            "Monitoring Service",
        ]

    def _generate_line_item(self) -> LineItem:
        """Generate a single line item with mathematically correct totals."""
        # Use whole numbers for services, allow decimals for products
        is_service = random.choice([True, False])

        if is_service:
            qty = float(random.randint(1, 20))
            price = round(random.uniform(75.00, 500.00), 2)
            desc = f"{random.choice(self.services)} - {fake.month_name()}"
        else:
            qty = round(random.uniform(1, 10), 1)
            price = round(random.uniform(25.00, 350.00), 2)
            desc = random.choice(self.products)

        total = round(qty * price, 2)

        return LineItem(
            description=desc,
            quantity=qty,
            unit_price=price,
            total=total
        )

    def generate_invoice(self) -> InvoiceData:
        """
        Create a completely synthetic invoice with valid data and calculations.

        Returns:
            InvoiceData object with all fields populated
        """
        # Generate date metadata
        inv_date = fake.date_between(start_date='-1y', end_date='today')
        due_date = inv_date + timedelta(days=random.choice([14, 30, 45, 60]))

        # Generate line items (3 to 8 items per invoice)
        items = [self._generate_line_item() for _ in range(random.randint(3, 8))]

        # Calculate totals with precision
        subtotal = sum(item.total for item in items)
        # UK VAT rates: 0% (zero-rated), 5% (reduced), 20% (standard)
        tax_rate = random.choice([0.0, 0.05, 0.20])
        tax_amt = round(subtotal * tax_rate, 2)
        grand_total = round(subtotal + tax_amt, 2)

        return InvoiceData(
            id=str(uuid.uuid4()),
            invoice_number=f"INV-{fake.bothify(text='####-????').upper()}",
            date=inv_date,
            due_date=due_date,
            sender_name=fake.company(),
            sender_address=fake.address().replace("\n", ", "),
            recipient_name=fake.name(),
            recipient_address=fake.address().replace("\n", ", "),
            line_items=items,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amt,
            total=grand_total,
            currency="GBP"
        )


# Quick test if run directly
if __name__ == "__main__":
    fab = DataFabricator()
    data = fab.generate_invoice()
    print(data.model_dump_json(indent=2))
