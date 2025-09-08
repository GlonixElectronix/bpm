from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Customer, ContactPerson, Quote, QuoteItem, CustomerDocument
from django.utils import timezone

class Command(BaseCommand):
    help = 'Load realistic demo data into all tables.'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='demo').exists():
            user = User.objects.create_user('demo', 'demo@example.com', 'demopassword')
            self.stdout.write(self.style.SUCCESS('Created demo user'))
        else:
            user = User.objects.get(username='demo')

        # Items
        from core.models import Item
        item1, _ = Item.objects.get_or_create(
            name='Widget A',
            defaults={
                'description': 'A widget',
                'price': 500.00,
                'sku': 'WIDGET-A-001',
            }
        )
        item2, _ = Item.objects.get_or_create(
            name='Widget B',
            defaults={
                'description': 'B widget',
                'price': 1000.00,
                'sku': 'WIDGET-B-002',
            }
        )
        item3, _ = Item.objects.get_or_create(
            name='Gadget X',
            defaults={
                'description': 'X gadget',
                'price': 800.00,
                'sku': 'GADGET-X-003',
            }
        )

        # Customers
        customer1, _ = Customer.objects.get_or_create(
            email='acme@example.com',
            defaults={
                'display_name': 'Acme Corp',
                'company_name': 'Acme Corporation',
                'billing_phone': '1234567890',
                'billing_street1': '123 Main St',
                'billing_city': 'Metropolis',
                'billing_state': 'State1',
                'billing_pin_code': '100001',
                'customer_type': 'business',
            }
        )
        customer2, _ = Customer.objects.get_or_create(
            email='globex@example.com',
            defaults={
                'display_name': 'Globex Inc',
                'company_name': 'Globex Incorporated',
                'billing_phone': '9876543210',
                'billing_street1': '456 Elm St',
                'billing_city': 'Gotham',
                'billing_state': 'State2',
                'billing_pin_code': '200002',
                'customer_type': 'business',
            }
        )

        # Contact Persons
        cp1, _ = ContactPerson.objects.get_or_create(
            customer=customer1,
            email='alice@acme.com',
            defaults={
                'first_name': 'Alice',
                'last_name': 'Smith',
                'work_phone': '1112223333',
                'mobile': '',
            }
        )
        cp2, _ = ContactPerson.objects.get_or_create(
            customer=customer1,
            email='bob@acme.com',
            defaults={
                'first_name': 'Bob',
                'last_name': 'Jones',
                'work_phone': '4445556666',
                'mobile': '',
            }
        )
        cp3, _ = ContactPerson.objects.get_or_create(
            customer=customer2,
            email='carol@globex.com',
            defaults={
                'first_name': 'Carol',
                'last_name': 'White',
                'work_phone': '7778889999',
                'mobile': '',
            }
        )

        # Quotes
        today = timezone.now().date()
        quote1, _ = Quote.objects.get_or_create(
            quote_number='Q-1001',
            defaults={
                'customer': customer1,
                'quote_date': today,
                'expiry_date': today,
                'customer_notes': 'Urgent delivery',
                'subtotal': 9000,
                'discount': 0,
                'tax_type': 'TDS',
                'tax_percentage': '0',
                'adjustment': 0,
                'total_amount': 10000,
            }
        )
        quote2, _ = Quote.objects.get_or_create(
            quote_number='Q-1002',
            defaults={
                'customer': customer2,
                'quote_date': today,
                'expiry_date': today,
                'customer_notes': 'Standard terms',
                'subtotal': 18000,
                'discount': 0,
                'tax_type': 'TDS',
                'tax_percentage': '0',
                'adjustment': 0,
                'total_amount': 20000,
            }
        )

        # Quote Items
        QuoteItem.objects.create(
            quote=quote1,
            item=item1,
            quantity=10,
            rate=500,
            amount=5000,
            quote_item_number=1,
        )
        QuoteItem.objects.create(
            quote=quote1,
            item=item2,
            quantity=5,
            rate=1000,
            amount=5000,
            quote_item_number=2,
        )
        QuoteItem.objects.create(
            quote=quote2,
            item=item3,
            quantity=20,
            rate=800,
            amount=16000,
            quote_item_number=1,
        )

        # Customer Documents (dummy entries, not real files)
        CustomerDocument.objects.create(
            file='customer_documents/testfile.txt',
            uploaded_at=timezone.now(),
        )
        CustomerDocument.objects.create(
            file='customer_documents/testfile_1TjmGU8.txt',
            uploaded_at=timezone.now(),
        )

        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully.'))


