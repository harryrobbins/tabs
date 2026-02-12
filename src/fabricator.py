import random
import uuid
from datetime import timedelta, datetime, time, date
from faker import Faker
from src.models import InvoiceData, LineItem, ReceiptData, ReceiptItem, BankStatementData, Transaction

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


class ReceiptFabricator:
    """Generates synthetic receipt data for retail/restaurant environments."""

    def __init__(self):
        """Initialize the receipt fabricator."""
        # Store types and their typical items
        self.store_types = {
            "cafe": {
                "name_formats": ["{} Coffee", "{} Cafe", "The {} Bean", "{} & Co"],
                "name_words": ["Corner", "Daily", "Morning", "Express", "Urban", "Artisan"],
                "items": [
                    "Cappuccino", "Latte", "Flat White", "Espresso", "Americano",
                    "Tea", "Hot Chocolate", "Croissant", "Muffin", "Sandwich",
                    "Pastry", "Cookie", "Scone", "Brownie", "Cake Slice"
                ]
            },
            "restaurant": {
                "name_formats": ["The {} Kitchen", "{} Grill", "{} Bistro", "{} & Spoon"],
                "name_words": ["Golden", "Red", "Green", "Royal", "Crown", "Oak"],
                "items": [
                    "Fish & Chips", "Burger & Fries", "Caesar Salad", "Soup of the Day",
                    "Shepherd's Pie", "Bangers & Mash", "Sunday Roast", "Steak",
                    "Chicken Tikka", "Pasta", "Pizza", "Side Salad", "Chips",
                    "Soft Drink", "Pint of Beer", "Glass of Wine", "Dessert"
                ]
            },
            "supermarket": {
                "name_formats": ["{} Market", "{} Supermarket", "{} Foods", "{} Stores"],
                "name_words": ["Fresh", "Value", "Quality", "Local", "Metro", "Express"],
                "items": [
                    "Bread", "Milk", "Eggs", "Butter", "Cheese", "Yoghurt",
                    "Apples", "Bananas", "Tomatoes", "Potatoes", "Carrots",
                    "Chicken Breast", "Bacon", "Pasta", "Rice", "Cereal",
                    "Orange Juice", "Coffee", "Tea Bags", "Biscuits", "Crisps"
                ]
            },
            "pharmacy": {
                "name_formats": ["{} Pharmacy", "{} Chemist", "{} Healthcare"],
                "name_words": ["Care", "Well", "Health", "Life", "Plus", "Cross"],
                "items": [
                    "Paracetamol", "Ibuprofen", "Plasters", "Bandages",
                    "Vitamins", "Cold Medicine", "Antiseptic Cream", "Eye Drops",
                    "Hand Sanitiser", "Tissues", "Toothpaste", "Shampoo",
                    "Soap", "Deodorant", "Moisturiser"
                ]
            },
            "petrol": {
                "name_formats": ["{} Petrol", "{} Service Station", "{} Fuel"],
                "name_words": ["Quick", "Express", "Auto", "Drive", "Fast", "Main"],
                "items": [
                    "Unleaded Petrol", "Diesel", "Premium Unleaded",
                    "Car Wash", "Screen Wash", "Oil", "Air Freshener",
                    "Snacks", "Drinks", "Sandwich", "Coffee"
                ]
            }
        }

        self.payment_methods = ["Card", "Cash", "Contactless", "Chip & PIN", "Mobile Pay"]

    def _generate_store_info(self):
        """Generate store name and type."""
        store_type = random.choice(list(self.store_types.keys()))
        store_data = self.store_types[store_type]

        name_format = random.choice(store_data["name_formats"])
        name_word = random.choice(store_data["name_words"])
        store_name = name_format.format(name_word)

        return store_name, store_type

    def _generate_receipt_item(self, store_type: str) -> ReceiptItem:
        """Generate a single receipt item based on store type."""
        items_list = self.store_types[store_type]["items"]
        description = random.choice(items_list)

        # Most items have quantity 1, some might have 2-3
        qty = float(random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0])

        # Price ranges vary by store type
        if store_type == "cafe":
            price = round(random.uniform(1.50, 8.50), 2)
        elif store_type == "restaurant":
            price = round(random.uniform(4.50, 25.00), 2)
        elif store_type == "supermarket":
            price = round(random.uniform(0.50, 12.00), 2)
        elif store_type == "pharmacy":
            price = round(random.uniform(1.99, 15.99), 2)
        elif store_type == "petrol":
            if "Petrol" in description or "Diesel" in description:
                # Petrol sold by litres at ~£1.40/L
                qty = round(random.uniform(20.0, 60.0), 2)
                price = 1.42
            else:
                price = round(random.uniform(0.99, 5.99), 2)

        total = round(qty * price, 2)

        return ReceiptItem(
            description=description,
            quantity=qty,
            unit_price=price,
            total=total
        )

    def generate_receipt(self) -> ReceiptData:
        """
        Create a completely synthetic receipt.

        Returns:
            ReceiptData object with all fields populated
        """
        # Generate store information
        store_name, store_type = self._generate_store_info()

        # Generate timestamp (within last 6 months, during business hours)
        base_date = fake.date_between(start_date='-6m', end_date='today')

        # Business hours: 7 AM to 10 PM
        hour = random.randint(7, 21)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        receipt_datetime = datetime.combine(base_date, time(hour, minute, second))

        # Generate items (2 to 8 items per receipt)
        num_items = random.randint(2, 8)
        items = [self._generate_receipt_item(store_type) for _ in range(num_items)]

        # Calculate totals
        subtotal = sum(item.total for item in items)
        tax_rate = 0.20  # UK standard VAT
        tax_amt = round(subtotal * tax_rate, 2)
        grand_total = round(subtotal + tax_amt, 2)

        # Payment method
        payment_method = random.choice(self.payment_methods)
        card_last_four = None
        if payment_method in ["Card", "Contactless", "Chip & PIN"]:
            card_last_four = f"{random.randint(0, 9999):04d}"

        return ReceiptData(
            id=str(uuid.uuid4()),
            receipt_number=f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            transaction_id=fake.bothify(text='TXN-########').upper(),
            datetime=receipt_datetime,
            store_name=store_name,
            store_address=fake.address().replace("\n", ", "),
            store_phone=fake.phone_number(),
            items=items,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amt,
            total=grand_total,
            payment_method=payment_method,
            card_last_four=card_last_four,
            currency="GBP"
        )


class BankStatementFabricator:
    """Generates synthetic bank statement data with multiple transactions."""

    def __init__(self):
        """Initialize the bank statement fabricator."""
        # UK banks
        self.banks = [
            {"name": "Barclays Bank PLC", "address": "1 Churchill Place, London, E14 5HP"},
            {"name": "HSBC UK Bank PLC", "address": "8 Canada Square, London, E14 5HQ"},
            {"name": "Lloyds Bank PLC", "address": "25 Gresham Street, London, EC2V 7HN"},
            {"name": "NatWest Bank PLC", "address": "250 Bishopsgate, London, EC2M 4AA"},
            {"name": "Santander UK PLC", "address": "2 Triton Square, London, NW1 3AN"},
        ]

        # Transaction types and descriptions
        self.transaction_types = {
            "salary": {
                "descriptions": ["SALARY PAYMENT", "MONTHLY SALARY", "PAYROLL"],
                "type": "credit",
                "amount_range": (1500, 5000)
            },
            "direct_debit": {
                "descriptions": [
                    "DD - BRITISH GAS",
                    "DD - THAMES WATER",
                    "DD - COUNCIL TAX",
                    "DD - MOBILE PHONE",
                    "DD - BROADBAND",
                    "DD - CAR INSURANCE",
                    "DD - HOME INSURANCE",
                    "DD - GYM MEMBERSHIP",
                    "DD - NETFLIX",
                    "DD - SPOTIFY"
                ],
                "type": "debit",
                "amount_range": (5, 150)
            },
            "card_purchase": {
                "descriptions": [
                    "TESCO STORES",
                    "SAINSBURY'S",
                    "ASDA SUPERSTORE",
                    "MORRISONS",
                    "MARKS & SPENCER",
                    "AMAZON.CO.UK",
                    "JOHN LEWIS",
                    "BOOTS",
                    "COSTA COFFEE",
                    "PRET A MANGER",
                    "WAITROSE",
                    "ARGOS",
                    "NEXT",
                    "H&M",
                    "ZARA",
                    "SHELL PETROL",
                    "BP FUEL",
                    "NANDOS",
                    "PIZZA EXPRESS",
                    "GREGGS"
                ],
                "type": "debit",
                "amount_range": (3, 200)
            },
            "atm_withdrawal": {
                "descriptions": ["ATM WITHDRAWAL", "CASH WITHDRAWAL"],
                "type": "debit",
                "amount_range": (20, 100)
            },
            "transfer_out": {
                "descriptions": [
                    "TRANSFER TO SAVINGS",
                    "TRANSFER TO J SMITH",
                    "TRANSFER TO S JONES"
                ],
                "type": "debit",
                "amount_range": (50, 500)
            },
            "transfer_in": {
                "descriptions": [
                    "TRANSFER FROM SAVINGS",
                    "BANK TRANSFER",
                    "FASTER PAYMENT"
                ],
                "type": "credit",
                "amount_range": (50, 1000)
            },
            "interest": {
                "descriptions": ["INTEREST PAID", "MONTHLY INTEREST"],
                "type": "credit",
                "amount_range": (0.50, 15)
            }
        }

    def _generate_transaction(self, current_date: date, balance: float) -> Transaction:
        """Generate a single transaction."""
        # Weighted selection - more card purchases and direct debits
        trans_type = random.choices(
            list(self.transaction_types.keys()),
            weights=[5, 15, 50, 8, 5, 5, 2],  # More common: card purchases, direct debits
            k=1
        )[0]

        trans_info = self.transaction_types[trans_type]
        description = random.choice(trans_info["descriptions"])

        # Generate amount
        min_amt, max_amt = trans_info["amount_range"]
        amount = round(random.uniform(min_amt, max_amt), 2)

        # Create transaction
        if trans_info["type"] == "debit":
            new_balance = balance - amount
            return Transaction(
                date=current_date,
                description=description,
                debit=amount,
                credit=None,
                balance=round(new_balance, 2)
            )
        else:  # credit
            new_balance = balance + amount
            return Transaction(
                date=current_date,
                description=description,
                debit=None,
                credit=amount,
                balance=round(new_balance, 2)
            )

    def generate_statement(self) -> BankStatementData:
        """
        Create a completely synthetic bank statement with 10-300 transactions.

        Returns:
            BankStatementData object with all fields populated
        """
        # Select bank
        bank = random.choice(self.banks)

        # Generate statement period (full month, 1-6 months ago)
        months_ago = random.randint(1, 6)
        end_date = (datetime.now() - timedelta(days=30 * months_ago)).date()
        # Set to last day of month
        if end_date.month == 12:
            end_date = end_date.replace(day=31)
        else:
            next_month = end_date.replace(month=end_date.month + 1, day=1)
            end_date = (next_month - timedelta(days=1))

        # Start date is first day of same month
        start_date = end_date.replace(day=1)

        # Statement date is a few days after period end
        statement_date = end_date + timedelta(days=random.randint(2, 5))

        # Generate number of transactions (10-300)
        num_transactions = random.randint(10, 300)

        # Opening balance
        opening_balance = round(random.uniform(100, 5000), 2)

        # Generate transactions
        transactions = []
        current_balance = opening_balance
        current_date = start_date

        for _ in range(num_transactions):
            # Random date within statement period
            days_in_period = (end_date - start_date).days + 1
            random_day = random.randint(0, days_in_period - 1)
            trans_date = start_date + timedelta(days=random_day)

            transaction = self._generate_transaction(trans_date, current_balance)
            current_balance = transaction.balance
            transactions.append(transaction)

        # Sort transactions by date
        transactions.sort(key=lambda t: t.date)

        # Recalculate balances in chronological order
        current_balance = opening_balance
        for trans in transactions:
            if trans.debit:
                current_balance -= trans.debit
            if trans.credit:
                current_balance += trans.credit
            trans.balance = round(current_balance, 2)

        closing_balance = current_balance

        # Generate account details
        sort_code = f"{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        account_number = f"****{random.randint(1000, 9999)}"

        return BankStatementData(
            id=str(uuid.uuid4()),
            account_holder_name=fake.name(),
            account_holder_address=fake.address().replace("\n", ", "),
            account_number=account_number,
            sort_code=sort_code,
            statement_period_start=start_date,
            statement_period_end=end_date,
            statement_date=statement_date,
            opening_balance=opening_balance,
            closing_balance=closing_balance,
            transactions=transactions,
            bank_name=bank["name"],
            bank_address=bank["address"],
            currency="GBP"
        )


# Quick test if run directly
if __name__ == "__main__":
    print("Testing Invoice Fabricator:")
    inv_fab = DataFabricator()
    invoice = inv_fab.generate_invoice()
    print(f"Generated invoice with {len(invoice.line_items)} items")

    print("\n" + "="*70 + "\n")
    print("Testing Receipt Fabricator:")
    rec_fab = ReceiptFabricator()
    receipt = rec_fab.generate_receipt()
    print(f"Generated receipt with {len(receipt.items)} items")

    print("\n" + "="*70 + "\n")
    print("Testing Bank Statement Fabricator:")
    bank_fab = BankStatementFabricator()
    statement = bank_fab.generate_statement()
    print(f"Generated statement with {len(statement.transactions)} transactions")
    print(f"Period: {statement.statement_period_start} to {statement.statement_period_end}")
    print(f"Opening balance: £{statement.opening_balance:.2f}")
    print(f"Closing balance: £{statement.closing_balance:.2f}")
