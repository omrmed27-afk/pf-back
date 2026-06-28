from django.test import TestCase
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.suppliers.models import Supplier

MOCK_PRODUCT = {
    "name": "Rollito Primavera",
    "sku": "ROL-001",
    "unit_price": "7.50",
    "stock": 30,
}


class ProductSerializerTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Prov Serializer", email="ser@prov.com")

    def test_valid_data_is_valid(self):
        serializer = ProductSerializer(data=MOCK_PRODUCT)
        self.assertTrue(serializer.is_valid())

    def test_contains_expected_fields(self):
        product = Product.objects.create(**{**MOCK_PRODUCT, "unit_price": 7.50})
        serializer = ProductSerializer(product)
        fields = set(serializer.data.keys())
        expected = {"id", "name", "description", "sku", "unit_price", "stock", "supplier", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_missing_name_is_invalid(self):
        data = {**MOCK_PRODUCT, "sku": "ERR-001"}
        data.pop("name")
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_sku_is_invalid(self):
        data = {**MOCK_PRODUCT}
        data.pop("sku")
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("sku", serializer.errors)

    def test_missing_unit_price_is_invalid(self):
        data = {**MOCK_PRODUCT, "sku": "ERR-002"}
        data.pop("unit_price")
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("unit_price", serializer.errors)

    def test_supplier_nullable(self):
        data = {**MOCK_PRODUCT, "sku": "NUL-001", "supplier": None}
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_with_valid_supplier(self):
        data = {**MOCK_PRODUCT, "sku": "SUP-001", "supplier": self.supplier.pk}
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
