from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.reservations.models import Reservation
from apps.reservations import services
from apps.customers.models import Customer
from apps.tables.models import Table
from apps.warehouses.models import Warehouse
import datetime

DATE = datetime.date(2026, 7, 15)
TIME = datetime.time(20, 0)


def make_fixtures():
    wh = Warehouse.objects.create(name="Local Svc", address="x", city="x", country="x", capacity=10)
    customer = Customer.objects.create(name="Cliente Svc", email="svc@test.com")
    table = Table.objects.create(warehouse=wh, number=1, capacity=4, status="available")
    return customer, table


class ReservationServicesTest(TestCase):

    def setUp(self):
        self.customer, self.table = make_fixtures()

    def test_create_reservation_available_table(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        self.assertIsNotNone(res.pk)

    def test_create_reservation_sets_table_to_reserved(self):
        services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        self.table.refresh_from_db()
        self.assertEqual(self.table.status, "reserved")

    def test_create_reservation_occupied_table_raises(self):
        self.table.status = "occupied"
        self.table.save()
        with self.assertRaises(ValidationError):
            services.create_reservation({
                "customer": self.customer, "table": self.table,
                "date": DATE, "time": TIME, "party_size": 2
            })

    def test_create_reservation_reserved_table_raises(self):
        self.table.status = "reserved"
        self.table.save()
        with self.assertRaises(ValidationError):
            services.create_reservation({
                "customer": self.customer, "table": self.table,
                "date": DATE, "time": TIME, "party_size": 2
            })

    def test_get_all_reservations(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        result = services.get_all_reservations()
        self.assertIn(res, result)

    def test_get_reservation_by_id(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        result = services.get_reservation_by_id(res.pk)
        self.assertEqual(result, res)

    def test_get_reservation_by_id_raises_on_missing(self):
        with self.assertRaises(Reservation.DoesNotExist):
            services.get_reservation_by_id(99999)

    def test_cancel_reservation_sets_cancelled(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        cancelled = services.cancel_reservation(res)
        self.assertEqual(cancelled.status, "cancelled")

    def test_cancel_reservation_frees_table(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        services.cancel_reservation(res)
        self.table.refresh_from_db()
        self.assertEqual(self.table.status, "available")

    def test_cancel_already_cancelled_raises(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        services.cancel_reservation(res)
        self.table.status = "available"
        self.table.save()
        with self.assertRaises(ValidationError):
            services.cancel_reservation(res)

    def test_update_reservation(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        updated = services.update_reservation(res, {"party_size": 5})
        self.assertEqual(updated.party_size, 5)

    def test_delete_reservation(self):
        res = services.create_reservation({
            "customer": self.customer, "table": self.table,
            "date": DATE, "time": TIME, "party_size": 2
        })
        pk = res.pk
        services.delete_reservation(res)
        self.assertFalse(Reservation.objects.filter(pk=pk).exists())
