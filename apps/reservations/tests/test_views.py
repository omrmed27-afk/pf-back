from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.reservations.models import Reservation
from apps.customers.models import Customer
from apps.tables.models import Table
from apps.warehouses.models import Warehouse
import datetime


def make_fixtures():
    wh = Warehouse.objects.create(name="Local Views", address="x", city="x", country="x", capacity=10)
    customer = Customer.objects.create(name="Cliente Views", email="views@test.com")
    table = Table.objects.create(warehouse=wh, number=1, capacity=4, status="available")
    return customer, table


class ReservationViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.customer, self.table = make_fixtures()
        self.reservation = Reservation.objects.create(
            customer=self.customer, table=self.table,
            date=datetime.date(2026, 8, 1), time=datetime.time(19, 0), party_size=2
        )
        self.url_list = "/api/v1/reservations/"
        self.url_detail = f"/api/v1/reservations/{self.reservation.id}/"
        self.url_cancel = f"/api/v1/reservations/{self.reservation.id}/cancel/"

    def _available_table(self):
        wh = Warehouse.objects.create(name="Extra", address="x", city="x", country="x", capacity=5)
        return Table.objects.create(warehouse=wh, number=1, capacity=4, status="available")

    # --- Happy path ---

    def test_list_reservations(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reservation_available_table(self):
        table2 = self._available_table()
        data = {
            "customer": self.customer.pk, "table": table2.pk,
            "date": "2026-09-01", "time": "20:00", "party_size": 3
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sets_table_reserved(self):
        table2 = self._available_table()
        data = {
            "customer": self.customer.pk, "table": table2.pk,
            "date": "2026-09-02", "time": "21:00", "party_size": 2
        }
        self.client.post(self.url_list, data, format="json")
        table2.refresh_from_db()
        self.assertEqual(table2.status, "reserved")

    def test_retrieve_reservation(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["party_size"], 2)

    def test_partial_update_reservation(self):
        response = self.client.patch(self.url_detail, {"party_size": 4}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["party_size"], 4)

    def test_cancel_reservation(self):
        response = self.client.post(self.url_cancel)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "cancelled")

    def test_cancel_frees_table(self):
        self.table.status = "reserved"
        self.table.save()
        self.client.post(self.url_cancel)
        self.table.refresh_from_db()
        self.assertEqual(self.table.status, "available")

    def test_delete_reservation(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Unhappy path ---

    def test_create_occupied_table_returns_400(self):
        self.table.status = "occupied"
        self.table.save()
        data = {
            "customer": self.customer.pk, "table": self.table.pk,
            "date": "2026-09-05", "time": "18:00", "party_size": 2
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_already_cancelled_returns_400(self):
        self.client.post(self.url_cancel)
        self.table.status = "available"
        self.table.save()
        response = self.client.post(self.url_cancel)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_customer_returns_400(self):
        data = {"table": self.table.pk, "date": "2026-09-10", "time": "19:00", "party_size": 2}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/reservations/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Reservation.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_notes(self):
        table2 = self._available_table()
        data = {
            "customer": self.customer.pk, "table": table2.pk,
            "date": "2026-09-20", "time": "20:30", "party_size": 2,
            "notes": "Alergia al maní"
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["notes"], "Alergia al maní")
