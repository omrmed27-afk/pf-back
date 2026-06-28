from django.test import TestCase
from apps.suppliers.models import Supplier

MOCK_SUPPLIER = {
    "name": "Proveedor Central",
    "email": "central@proveedor.com",
    "phone": "1122334455",
    "address": "Calle Comercio 500",
    "contact_name": "Juan García",
}


class SupplierModelTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(**MOCK_SUPPLIER)

    def test_create_supplier(self):
        self.assertEqual(self.supplier.name, "Proveedor Central")
        self.assertEqual(self.supplier.contact_name, "Juan García")

    def test_str_returns_name(self):
        self.assertEqual(str(self.supplier), "Proveedor Central")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.supplier.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.supplier.updated_at)

    def test_optional_fields_can_be_empty(self):
        supplier = Supplier.objects.create(name="Solo Nombre")
        self.assertEqual(supplier.email, "")
        self.assertEqual(supplier.phone, "")
        self.assertEqual(supplier.address, "")
        self.assertEqual(supplier.contact_name, "")
