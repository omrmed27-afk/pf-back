from django.test import TestCase
from django.db import IntegrityError
from apps.products.models import Product
from apps.suppliers.models import Supplier

MOCK_SUPPLIER = {"name": "Proveedor Test", "email": "prov@test.com"}
MOCK_PRODUCT = {
    "name": "Arroz Frito Especial",
    "description": "Arroz con verduras y salsa de soja",
    "sku": "ARR-001",
    "unit_price": 12.50,
    "stock": 20,
}


class ProductModelTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(**MOCK_SUPPLIER)
        self.product = Product.objects.create(**MOCK_PRODUCT, supplier=self.supplier)

    def test_create_product(self):
        self.assertEqual(self.product.name, "Arroz Frito Especial")
        self.assertEqual(self.product.sku, "ARR-001")
        self.assertEqual(float(self.product.unit_price), 12.50)

    def test_str_returns_name_and_sku(self):
        self.assertEqual(str(self.product), "Arroz Frito Especial (ARR-001)")

    def test_sku_is_unique(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Otro", sku="ARR-001", unit_price=5.00)

    def test_supplier_is_nullable(self):
        product = Product.objects.create(name="Sin Proveedor", sku="SP-001", unit_price=8.00)
        self.assertIsNone(product.supplier)

    def test_supplier_set_null_on_delete(self):
        self.supplier.delete()
        self.product.refresh_from_db()
        self.assertIsNone(self.product.supplier)

    def test_default_stock_is_zero(self):
        product = Product.objects.create(name="Stock Default", sku="SD-001", unit_price=5.00)
        self.assertEqual(product.stock, 0)

    def test_description_nullable(self):
        product = Product.objects.create(name="Sin Desc", sku="ND-001", unit_price=3.00, description=None)
        self.assertIsNone(product.description)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.product.created_at)
