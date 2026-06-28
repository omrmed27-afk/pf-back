from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.tables.models import Table
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="Local Views", address="x", city="x", country="x", capacity=20)


class TableViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.warehouse = make_warehouse()
        self.table = Table.objects.create(warehouse=self.warehouse, number=1, capacity=4, status="available")
        self.url_list = "/api/v1/tables/"
        self.url_detail = f"/api/v1/tables/{self.table.id}/"
        self.url_status = f"/api/v1/tables/{self.table.id}/change-status/"

    # --- Happy path ---

    def test_list_tables(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_table(self):
        data = {"warehouse": self.warehouse.pk, "number": 2, "capacity": 6}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["number"], 2)

    def test_retrieve_table(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], 1)

    def test_update_table(self):
        data = {"warehouse": self.warehouse.pk, "number": 1, "capacity": 10, "status": "available"}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["capacity"], 10)

    def test_partial_update_table(self):
        response = self.client.patch(self.url_detail, {"capacity": 8}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["capacity"], 8)

    def test_delete_table(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Table.objects.filter(id=self.table.id).exists())

    # --- Change status endpoint ---

    def test_change_status_available_to_reserved(self):
        response = self.client.post(self.url_status, {"status": "reserved"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "reserved")

    def test_change_status_invalid_transition_returns_400(self):
        response = self.client.post(self.url_status, {"status": "occupied"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_status_missing_field_returns_400(self):
        response = self.client.post(self.url_status, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_cycle_available_reserved_occupied_available(self):
        self.client.post(self.url_status, {"status": "reserved"}, format="json")
        self.client.post(self.url_status, {"status": "occupied"}, format="json")
        response = self.client.post(self.url_status, {"status": "available"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "available")

    # --- Unhappy path ---

    def test_create_duplicate_number_same_warehouse_returns_400(self):
        data = {"warehouse": self.warehouse.pk, "number": 1, "capacity": 2}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/tables/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Table.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_same_number_different_warehouse_allowed(self):
        wh2 = Warehouse.objects.create(name="Local 2", address="x", city="x", country="x", capacity=5)
        data = {"warehouse": wh2.pk, "number": 1, "capacity": 4}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
