from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.products.models import Product
from apps.suppliers.models import Supplier

MOCK_PRODUCT = {
    "name": "Wonton Sopa",
    "sku": "WON-001",
    "unit_price": "8.50",
    "stock": 25,
}


class ProductViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.supplier = Supplier.objects.create(name="Prov Views", email="views@prov.com")
        self.product = Product.objects.create(
            name="Wonton Sopa", sku="WON-001", unit_price=8.50, stock=25, supplier=self.supplier
        )
        self.url_list = "/api/v1/products/"
        self.url_detail = f"/api/v1/products/{self.product.id}/"

    # --- Happy path ---

    def test_list_products(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        data = {"name": "Pato Laqueado", "sku": "PAT-001", "unit_price": "15.00", "stock": 10}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["sku"], "PAT-001")

    def test_create_product_with_supplier(self):
        data = {"name": "Sopa Miso", "sku": "MIS-001", "unit_price": "5.00", "supplier": self.supplier.pk}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["supplier"], self.supplier.pk)

    def test_retrieve_product(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["sku"], "WON-001")

    def test_update_product(self):
        data = {"name": "Wonton Sopa", "sku": "WON-001", "unit_price": "10.00", "stock": 50}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stock"], 50)

    def test_partial_update_product(self):
        response = self.client.patch(self.url_detail, {"stock": 99}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stock"], 99)

    def test_delete_product(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    # --- Unhappy path ---

    def test_create_without_name_returns_400(self):
        data = {"sku": "ERR-001", "unit_price": "5.00"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_sku_returns_400(self):
        data = {"name": "Sin SKU", "unit_price": "5.00"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_price_returns_400(self):
        data = {"name": "Sin Precio", "sku": "SP-001"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_sku_returns_400(self):
        data = {"name": "Duplicado", "sku": "WON-001", "unit_price": "5.00"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/products/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Product.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_null_supplier(self):
        data = {"name": "Sin Proveedor", "sku": "SP-999", "unit_price": "3.00", "supplier": None}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["supplier"])

    def test_list_ordered_by_name(self):
        Product.objects.create(name="AAA Plato", sku="AAA-V", unit_price=1.00)
        Product.objects.create(name="ZZZ Plato", sku="ZZZ-V", unit_price=1.00)
        response = self.client.get(self.url_list)
        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names, sorted(names))
