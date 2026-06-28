from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.customers.models import Customer

MOCK_CUSTOMER = {
    "name": "Cliente Oeste",
    "email": "oeste@cliente.com",
    "phone": "5544332211",
    "address": "Calle Oeste 300",
    "customer_type": "individual",
    "tax_id": None,
}


class CustomerViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.customer = Customer.objects.create(
            name="Cliente Oeste",
            email="oeste@cliente.com",
            phone="5544332211",
            address="Calle Oeste 300",
            customer_type="individual",
        )
        self.url_list = "/api/v1/customers/"
        self.url_detail = f"/api/v1/customers/{self.customer.id}/"

    # --- Happy path ---

    def test_list_customers(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        data = {"name": "Nuevo Cliente", "email": "nuevo@cliente.com", "customer_type": "company"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Nuevo Cliente")

    def test_retrieve_customer(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "oeste@cliente.com")

    def test_update_customer(self):
        data = {"name": "Cliente Oeste", "email": "oeste@cliente.com", "customer_type": "company"}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["customer_type"], "company")

    def test_partial_update_customer(self):
        response = self.client.patch(self.url_detail, {"phone": "0000000000"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "0000000000")

    def test_delete_customer(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())

    # --- Unhappy path ---

    def test_create_without_name_returns_400(self):
        response = self.client.post(self.url_list, {"email": "sin@nombre.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_email_returns_400(self):
        response = self.client.post(self.url_list, {"name": "Sin Email"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_email_returns_400(self):
        data = {"name": "Duplicado", "email": "oeste@cliente.com"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_customer_type_returns_400(self):
        data = {"name": "Tipo Inválido", "email": "tipo@test.com", "customer_type": "vip"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/customers/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Customer.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_null_tax_id(self):
        data = {"name": "Sin Tax", "email": "sintax@test.com", "tax_id": None}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["tax_id"])

    def test_list_ordered_by_name(self):
        Customer.objects.create(name="AAA Cliente", email="aaa@test.com")
        Customer.objects.create(name="ZZZ Cliente", email="zzz@test.com")
        response = self.client.get(self.url_list)
        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names))
