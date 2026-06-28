from django.test import TestCase
from apps.suppliers.models import Supplier
from apps.suppliers.serializers import SupplierSerializer

MOCK_SUPPLIER = {
    "name": "Proveedor Norte",
    "email": "norte@proveedor.com",
    "phone": "9988776655",
    "address": "Av. Industrial 200",
    "contact_name": "María López",
}


class SupplierSerializerTest(TestCase):

    def test_valid_data_is_valid(self):
        serializer = SupplierSerializer(data=MOCK_SUPPLIER)
        self.assertTrue(serializer.is_valid())

    def test_only_name_is_required(self):
        serializer = SupplierSerializer(data={"name": "Mínimo"})
        self.assertTrue(serializer.is_valid())

    def test_serializer_contains_expected_fields(self):
        supplier = Supplier.objects.create(**MOCK_SUPPLIER)
        serializer = SupplierSerializer(supplier)
        fields = set(serializer.data.keys())
        expected = {"id", "name", "email", "phone", "address", "contact_name", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_missing_name_is_invalid(self):
        data = {**MOCK_SUPPLIER}
        data.pop("name")
        serializer = SupplierSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_empty_name_is_invalid(self):
        data = {**MOCK_SUPPLIER, "name": ""}
        serializer = SupplierSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_email_format_is_invalid(self):
        data = {**MOCK_SUPPLIER, "email": "no-es-email"}
        serializer = SupplierSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
