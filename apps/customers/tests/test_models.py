from django.test import TestCase
from django.db import IntegrityError
from apps.customers.models import Customer

MOCK_CUSTOMER = {
    "name": "Cliente Central",
    "email": "cliente@central.com",
    "phone": "1122334455",
    "address": "Av. Siempre Viva 742",
    "customer_type": "individual",
    "tax_id": "20-12345678-9",
}


class CustomerModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(**MOCK_CUSTOMER)

    def test_create_customer(self):
        self.assertEqual(self.customer.name, "Cliente Central")
        self.assertEqual(self.customer.customer_type, "individual")

    def test_str_returns_name(self):
        self.assertEqual(str(self.customer), "Cliente Central")

    def test_email_is_unique(self):
        with self.assertRaises(IntegrityError):
            Customer.objects.create(name="Duplicado", email="cliente@central.com")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.customer.created_at)

    def test_optional_fields_can_be_empty(self):
        customer = Customer.objects.create(name="Mínimo", email="minimo@test.com")
        self.assertEqual(customer.phone, "")
        self.assertEqual(customer.address, "")
        self.assertIsNone(customer.tax_id)

    def test_default_customer_type_is_individual(self):
        customer = Customer.objects.create(name="Default", email="default@test.com")
        self.assertEqual(customer.customer_type, "individual")

    def test_company_type_valid(self):
        customer = Customer.objects.create(name="Empresa SA", email="empresa@test.com", customer_type="company")
        self.assertEqual(customer.customer_type, "company")
