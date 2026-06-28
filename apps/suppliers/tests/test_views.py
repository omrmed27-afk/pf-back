from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.suppliers.models import Supplier

MOCK_SUPPLIER = {
    "name": "Proveedor Oeste",
    "email": "oeste@proveedor.com",
    "phone": "5544332211",
    "address": "Calle Oeste 300",
    "contact_name": "Ana Pérez",
}


class SupplierViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.supplier = Supplier.objects.create(**MOCK_SUPPLIER)
        self.url_list = "/api/v1/suppliers/"
        self.url_detail = f"/api/v1/suppliers/{self.supplier.id}/"

    # --- Happy path ---

    def test_list_suppliers(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        data = {"name": "Nuevo Proveedor", "email": "nuevo@proveedor.com"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Nuevo Proveedor")

    def test_retrieve_supplier(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], MOCK_SUPPLIER["name"])

    def test_update_supplier(self):
        data = {**MOCK_SUPPLIER, "contact_name": "Roberto Gómez"}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["contact_name"], "Roberto Gómez")

    def test_partial_update_supplier(self):
        response = self.client.patch(self.url_detail, {"phone": "9999999999"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "9999999999")

    def test_delete_supplier(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Supplier.objects.filter(id=self.supplier.id).exists())

    # --- Unhappy path ---

    def test_create_without_name_returns_400(self):
        data = {"email": "sinombre@test.com"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_invalid_email_returns_400(self):
        data = {**MOCK_SUPPLIER, "name": "Test Email", "email": "no-es-email"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/suppliers/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Supplier.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_only_name(self):
        response = self.client.post(self.url_list, {"name": "Solo Nombre"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_ordered_by_name(self):
        Supplier.objects.create(name="AAA Proveedor")
        Supplier.objects.create(name="ZZZ Proveedor")
        response = self.client.get(self.url_list)
        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names))
