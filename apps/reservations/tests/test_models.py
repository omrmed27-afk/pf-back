from django.test import TestCase
from apps.reservations.models import Reservation
from apps.customers.models import Customer
from apps.tables.models import Table
from apps.warehouses.models import Warehouse
import datetime


def make_fixtures():
    wh = Warehouse.objects.create(name="Local", address="x", city="x", country="x", capacity=10)
    customer = Customer.objects.create(name="Cliente Test", email="ct@test.com")
    table = Table.objects.create(warehouse=wh, number=1, capacity=4)
    return customer, table


class ReservationModelTest(TestCase):

    def setUp(self):
        self.customer, self.table = make_fixtures()
        self.reservation = Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            date=datetime.date(2026, 7, 1),
            time=datetime.time(20, 0),
            party_size=3,
        )

    def test_create_reservation(self):
        self.assertEqual(self.reservation.customer, self.customer)
        self.assertEqual(self.reservation.table, self.table)
        self.assertEqual(self.reservation.party_size, 3)

    def test_str_format(self):
        self.assertIn("Cliente Test", str(self.reservation))
        self.assertIn("2026-07-01", str(self.reservation))

    def test_default_status_is_pending(self):
        self.assertEqual(self.reservation.status, "pending")

    def test_notes_nullable(self):
        self.assertIsNone(self.reservation.notes)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.reservation.created_at)
