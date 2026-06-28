from django.test import TestCase
from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationSerializer
from apps.customers.models import Customer
from apps.tables.models import Table
from apps.warehouses.models import Warehouse
import datetime


def make_fixtures():
    wh = Warehouse.objects.create(name="Local Ser", address="x", city="x", country="x", capacity=10)
    customer = Customer.objects.create(name="Cliente Ser", email="ser@test.com")
    table = Table.objects.create(warehouse=wh, number=1, capacity=4)
    return customer, table


class ReservationSerializerTest(TestCase):

    def setUp(self):
        self.customer, self.table = make_fixtures()

    def test_valid_data_is_valid(self):
        data = {
            "customer": self.customer.pk,
            "table": self.table.pk,
            "date": "2026-07-10",
            "time": "19:00",
            "party_size": 2,
        }
        serializer = ReservationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contains_expected_fields(self):
        res = Reservation.objects.create(
            customer=self.customer, table=self.table,
            date=datetime.date(2026, 7, 1), time=datetime.time(20, 0), party_size=2
        )
        serializer = ReservationSerializer(res)
        expected = {"id", "customer", "table", "date", "time", "party_size", "status", "notes", "created_at", "updated_at"}
        self.assertEqual(set(serializer.data.keys()), expected)

    def test_missing_customer_is_invalid(self):
        data = {"table": self.table.pk, "date": "2026-07-10", "time": "19:00", "party_size": 2}
        serializer = ReservationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)

    def test_missing_date_is_invalid(self):
        data = {"customer": self.customer.pk, "table": self.table.pk, "time": "19:00", "party_size": 2}
        serializer = ReservationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("date", serializer.errors)

    def test_invalid_status_is_invalid(self):
        data = {
            "customer": self.customer.pk, "table": self.table.pk,
            "date": "2026-07-10", "time": "19:00", "party_size": 2, "status": "vip"
        }
        serializer = ReservationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_notes_optional(self):
        data = {
            "customer": self.customer.pk, "table": self.table.pk,
            "date": "2026-07-10", "time": "19:00", "party_size": 2, "notes": None
        }
        serializer = ReservationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
