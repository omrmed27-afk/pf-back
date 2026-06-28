from django.test import TestCase
from apps.warehouses.models import Warehouse
from apps.warehouses.serializers import WarehouseSerializer

MOCK_WAREHOUSE = {
    "name": "Sucursal Norte",
    "address": "Calle Falsa 742",
    "city": "Córdoba",
    "country": "Argentina",
    "capacity": 100,
}


class WarehouseSerializerTest(TestCase):

    def test_valid_data_is_valid(self):
        serializer = WarehouseSerializer(data=MOCK_WAREHOUSE)
        self.assertTrue(serializer.is_valid())

    def test_serializer_contains_expected_fields(self):
        warehouse = Warehouse.objects.create(**MOCK_WAREHOUSE)
        serializer = WarehouseSerializer(warehouse)
        fields = set(serializer.data.keys())
        expected = {"id", "name", "address", "city", "country", "capacity", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_missing_name_is_invalid(self):
        data = {**MOCK_WAREHOUSE}
        data.pop("name")
        serializer = WarehouseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_address_is_invalid(self):
        data = {**MOCK_WAREHOUSE}
        data.pop("address")
        serializer = WarehouseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("address", serializer.errors)

    def test_missing_capacity_is_invalid(self):
        data = {**MOCK_WAREHOUSE}
        data.pop("capacity")
        serializer = WarehouseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("capacity", serializer.errors)

    def test_capacity_string_is_invalid(self):
        data = {**MOCK_WAREHOUSE, "capacity": "mucho"}
        serializer = WarehouseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("capacity", serializer.errors)

    def test_empty_name_is_invalid(self):
        data = {**MOCK_WAREHOUSE, "name": ""}
        serializer = WarehouseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
