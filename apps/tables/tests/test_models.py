from django.test import TestCase
from django.db import IntegrityError
from apps.tables.models import Table
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="Local Modelo", address="x", city="x", country="x", capacity=10)


class TableModelTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.table = Table.objects.create(warehouse=self.warehouse, number=1, capacity=4)

    def test_create_table(self):
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertEqual(self.table.warehouse, self.warehouse)

    def test_str_returns_number_and_warehouse(self):
        self.assertEqual(str(self.table), "Mesa 1 - Local Modelo")

    def test_default_status_is_available(self):
        self.assertEqual(self.table.status, "available")

    def test_unique_together_warehouse_number(self):
        with self.assertRaises(IntegrityError):
            Table.objects.create(warehouse=self.warehouse, number=1, capacity=6)

    def test_same_number_different_warehouse_allowed(self):
        wh2 = Warehouse.objects.create(name="Local 2", address="x", city="x", country="x", capacity=5)
        t2 = Table.objects.create(warehouse=wh2, number=1, capacity=4)
        self.assertIsNotNone(t2.pk)

    def test_table_deleted_on_warehouse_delete(self):
        pk = self.table.pk
        self.warehouse.delete()
        self.assertFalse(Table.objects.filter(pk=pk).exists())

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.table.created_at)
