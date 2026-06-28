from django.test import TestCase
from apps.tables.models import Table
from apps.tables.serializers import TableSerializer
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="Local Ser", address="x", city="x", country="x", capacity=10)


class TableSerializerTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.table = Table.objects.create(warehouse=self.warehouse, number=1, capacity=4)

    def test_valid_data_is_valid(self):
        data = {"warehouse": self.warehouse.pk, "number": 2, "capacity": 6, "status": "available"}
        serializer = TableSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contains_expected_fields(self):
        serializer = TableSerializer(self.table)
        fields = set(serializer.data.keys())
        expected = {"id", "warehouse", "number", "capacity", "status", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_missing_warehouse_is_invalid(self):
        data = {"number": 3, "capacity": 2}
        serializer = TableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("warehouse", serializer.errors)

    def test_missing_number_is_invalid(self):
        data = {"warehouse": self.warehouse.pk, "capacity": 2}
        serializer = TableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("number", serializer.errors)

    def test_missing_capacity_is_invalid(self):
        data = {"warehouse": self.warehouse.pk, "number": 4}
        serializer = TableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("capacity", serializer.errors)

    def test_invalid_status_is_invalid(self):
        data = {"warehouse": self.warehouse.pk, "number": 5, "capacity": 4, "status": "cerrada"}
        serializer = TableSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
