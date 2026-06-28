from django.test import TestCase
from apps.warehouses.models import Warehouse

MOCK_WAREHOUSE = {
    "name": "Sucursal Centro",
    "address": "Av. Principal 123",
    "city": "Buenos Aires",
    "country": "Argentina",
    "capacity": 50,
}


class WarehouseModelTest(TestCase):

    def setUp(self):
        self.warehouse = Warehouse.objects.create(**MOCK_WAREHOUSE)

    def test_create_warehouse(self):
        self.assertEqual(self.warehouse.name, "Sucursal Centro")
        self.assertEqual(self.warehouse.city, "Buenos Aires")
        self.assertEqual(self.warehouse.capacity, 50)

    def test_str_returns_name(self):
        self.assertEqual(str(self.warehouse), "Sucursal Centro")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.warehouse.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.warehouse.updated_at)

    def test_capacity_is_integer(self):
        self.assertIsInstance(self.warehouse.capacity, int)
