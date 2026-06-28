from django.test import TestCase
from apps.products.models import Product
from apps.products import services
from apps.suppliers.models import Supplier

MOCK_PRODUCT = {
    "name": "Dim Sum",
    "sku": "DIM-001",
    "unit_price": 9.00,
    "stock": 15,
}


class ProductServicesTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Prov Svc", email="svc@prov.com")
        self.product = Product.objects.create(**MOCK_PRODUCT, supplier=self.supplier)

    def test_get_all_products_returns_queryset(self):
        result = services.get_all_products()
        self.assertIn(self.product, result)

    def test_get_all_products_ordered_by_name(self):
        Product.objects.create(name="AAA Plato", sku="AAA-001", unit_price=1.00)
        Product.objects.create(name="ZZZ Plato", sku="ZZZ-001", unit_price=1.00)
        result = list(services.get_all_products())
        names = [p.name for p in result]
        self.assertEqual(names, sorted(names))

    def test_get_product_by_id(self):
        result = services.get_product_by_id(self.product.pk)
        self.assertEqual(result, self.product)

    def test_get_product_by_id_raises_on_missing(self):
        with self.assertRaises(Product.DoesNotExist):
            services.get_product_by_id(99999)

    def test_create_product(self):
        data = {"name": "Nuevo Plato", "sku": "NP-001", "unit_price": 11.00}
        product = services.create_product(data)
        self.assertTrue(Product.objects.filter(pk=product.pk).exists())

    def test_update_product(self):
        updated = services.update_product(self.product, {"stock": 50})
        self.assertEqual(updated.stock, 50)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 50)

    def test_delete_product(self):
        pk = self.product.pk
        services.delete_product(self.product)
        self.assertFalse(Product.objects.filter(pk=pk).exists())
