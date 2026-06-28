from django.test import TestCase
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer

MOCK_CUSTOMER = {
    "name": "Cliente Norte",
    "email": "norte@cliente.com",
    "phone": "9988776655",
    "address": "Calle Norte 100",
    "customer_type": "company",
    "tax_id": "30-98765432-1",
}


class CustomerSerializerTest(TestCase):

    def test_valid_data_is_valid(self):
        serializer = CustomerSerializer(data=MOCK_CUSTOMER)
        self.assertTrue(serializer.is_valid())

    def test_serializer_contains_expected_fields(self):
        customer = Customer.objects.create(**MOCK_CUSTOMER)
        serializer = CustomerSerializer(customer)
        fields = set(serializer.data.keys())
        expected = {"id", "name", "email", "phone", "address", "customer_type", "tax_id", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_missing_name_is_invalid(self):
        data = {**MOCK_CUSTOMER, "email": "otro@test.com"}
        data.pop("name")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_email_is_invalid(self):
        data = {**MOCK_CUSTOMER}
        data.pop("email")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_invalid_email_format_is_invalid(self):
        data = {**MOCK_CUSTOMER, "email": "no-es-email"}
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_invalid_customer_type_is_invalid(self):
        data = {**MOCK_CUSTOMER, "email": "tipo@test.com", "customer_type": "vip"}
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer_type", serializer.errors)

    def test_tax_id_nullable(self):
        data = {**MOCK_CUSTOMER, "email": "notaxid@test.com", "tax_id": None}
        serializer = CustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
