from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.warehouses.models import Warehouse

MOCK_WAREHOUSE = {
    "name": "Sucursal Sur",
    "address": "Ruta 9 Km 50",
    "city": "Rosario",
    "country": "Argentina",
    "capacity": 200,
}


class WarehouseViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.warehouse = Warehouse.objects.create(**MOCK_WAREHOUSE)
        self.url_list = "/api/v1/warehouses/"
        self.url_detail = f"/api/v1/warehouses/{self.warehouse.id}/"

    # --- Happy path ---

    def test_list_warehouses(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_warehouse(self):
        data = {
            "name": "Sucursal Este",
            "address": "Av. Libertador 999",
            "city": "Mendoza",
            "country": "Argentina",
            "capacity": 75,
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Sucursal Este")

    def test_retrieve_warehouse(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], MOCK_WAREHOUSE["name"])

    def test_update_warehouse(self):
        data = {**MOCK_WAREHOUSE, "capacity": 300}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["capacity"], 300)

    def test_partial_update_warehouse(self):
        response = self.client.patch(self.url_detail, {"city": "Tucumán"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "Tucumán")

    def test_delete_warehouse(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Warehouse.objects.filter(id=self.warehouse.id).exists())

    # --- Unhappy path ---

    def test_create_without_name_returns_400(self):
        data = {**MOCK_WAREHOUSE}
        data.pop("name")
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_capacity_returns_400(self):
        data = {**MOCK_WAREHOUSE}
        data.pop("capacity")
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/warehouses/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_invalid_capacity_returns_400(self):
        data = {**MOCK_WAREHOUSE, "capacity": "invalido"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Warehouse.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_ordered_by_name(self):
        Warehouse.objects.create(name="AAA Almacen", address="x", city="x", country="x", capacity=1)
        Warehouse.objects.create(name="ZZZ Almacen", address="x", city="x", country="x", capacity=1)
        response = self.client.get(self.url_list)
        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names))

    def test_create_with_zero_capacity(self):
        data = {**MOCK_WAREHOUSE, "name": "Micro Sucursal", "capacity": 0}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
