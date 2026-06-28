from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.tables.models import Table
from apps.tables import services
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="Local Svc", address="x", city="x", country="x", capacity=10)


class TableServicesTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.table = Table.objects.create(warehouse=self.warehouse, number=1, capacity=4, status="available")

    def test_get_all_tables(self):
        result = services.get_all_tables()
        self.assertIn(self.table, result)

    def test_get_table_by_id(self):
        result = services.get_table_by_id(self.table.pk)
        self.assertEqual(result, self.table)

    def test_get_table_by_id_raises_on_missing(self):
        with self.assertRaises(Table.DoesNotExist):
            services.get_table_by_id(99999)

    def test_create_table(self):
        table = services.create_table({"warehouse": self.warehouse, "number": 2, "capacity": 2})
        self.assertTrue(Table.objects.filter(pk=table.pk).exists())

    def test_update_table(self):
        updated = services.update_table(self.table, {"capacity": 8})
        self.assertEqual(updated.capacity, 8)

    def test_delete_table(self):
        pk = self.table.pk
        services.delete_table(self.table)
        self.assertFalse(Table.objects.filter(pk=pk).exists())

    # --- Ciclo de estados ---

    def test_available_to_reserved(self):
        result = services.change_status(self.table, "reserved")
        self.assertEqual(result.status, "reserved")

    def test_reserved_to_occupied(self):
        self.table.status = "reserved"
        self.table.save()
        result = services.change_status(self.table, "occupied")
        self.assertEqual(result.status, "occupied")

    def test_occupied_to_available(self):
        self.table.status = "occupied"
        self.table.save()
        result = services.change_status(self.table, "available")
        self.assertEqual(result.status, "available")

    def test_reserved_to_available(self):
        self.table.status = "reserved"
        self.table.save()
        result = services.change_status(self.table, "available")
        self.assertEqual(result.status, "available")

    def test_available_to_occupied_raises(self):
        with self.assertRaises(ValidationError):
            services.change_status(self.table, "occupied")

    def test_occupied_to_reserved_raises(self):
        self.table.status = "occupied"
        self.table.save()
        with self.assertRaises(ValidationError):
            services.change_status(self.table, "reserved")

    def test_same_status_raises(self):
        with self.assertRaises(ValidationError):
            services.change_status(self.table, "available")
