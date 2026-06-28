import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.shipments.models import Shipment, ShipmentProduct
from .fixtures import make_all, make_shipment

BASE_DATA = {
    "destination_address": "Calle Entrega 200",
    "destination_city": "Córdoba",
    "estimated_delivery_date": "2026-10-01T18:00:00Z",
}


class ShipmentViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.fx = make_all()
        self.shipment = make_shipment(self.fx["customer"], self.fx["warehouse"])
        self.url_list = "/api/v1/shipments/"
        self.url_detail = f"/api/v1/shipments/{self.shipment.id}/"
        self.url_dispatch = f"/api/v1/shipments/{self.shipment.id}/dispatch/"
        self.url_deliver = f"/api/v1/shipments/{self.shipment.id}/deliver/"
        self.url_cancel = f"/api/v1/shipments/{self.shipment.id}/cancel/"
        self.url_return = f"/api/v1/shipments/{self.shipment.id}/return/"

    # --- Happy path ---

    def test_list_shipments(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shipment(self):
        data = {**BASE_DATA, "customer": self.fx["customer"].pk, "origin_warehouse": self.fx["warehouse"].pk}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["tracking_number"].startswith("SHIP-"))

    def test_retrieve_shipment(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "pending")

    def test_retrieve_has_nested_products(self):
        ShipmentProduct.objects.create(
            shipment=self.shipment, product=self.fx["product"], quantity=1, unit_price=10.00
        )
        response = self.client.get(self.url_detail)
        self.assertEqual(len(response.data["shipment_products"]), 1)

    def test_partial_update_shipment(self):
        response = self.client.patch(self.url_detail, {"destination_city": "Mendoza"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["destination_city"], "Mendoza")

    def test_delete_shipment(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_dispatch_shipment(self):
        data = {
            "driver": self.fx["driver"].pk,
            "transport": self.fx["transport"].pk,
            "route": self.fx["route"].pk,
        }
        response = self.client.post(self.url_dispatch, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "in_transit")

    def test_deliver_shipment(self):
        self.shipment.status = "in_transit"
        self.shipment.save()
        response = self.client.post(self.url_deliver)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "delivered")

    def test_cancel_shipment(self):
        response = self.client.post(self.url_cancel)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "cancelled")

    def test_return_shipment(self):
        self.shipment.status = "in_transit"
        self.shipment.save()
        response = self.client.post(self.url_return)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "returned")

    # --- Unhappy path ---

    def test_dispatch_missing_fields_returns_400(self):
        response = self.client.post(self.url_dispatch, {"driver": self.fx["driver"].pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dispatch_invalid_transition_returns_400(self):
        self.shipment.status = "delivered"
        self.shipment.save()
        data = {"driver": self.fx["driver"].pk, "transport": self.fx["transport"].pk, "route": self.fx["route"].pk}
        response = self.client.post(self.url_dispatch, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deliver_invalid_transition_returns_400(self):
        response = self.client.post(self.url_deliver)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_cancelled_returns_400(self):
        self.shipment.status = "cancelled"
        self.shipment.save()
        response = self.client.post(self.url_cancel)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_customer_returns_400(self):
        data = {**BASE_DATA, "origin_warehouse": self.fx["warehouse"].pk}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/shipments/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Shipment.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tracking_number_not_overwritable(self):
        data = {**BASE_DATA, "customer": self.fx["customer"].pk,
                "origin_warehouse": self.fx["warehouse"].pk, "tracking_number": "FAKE-0001"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["tracking_number"], "FAKE-0001")

    def test_dispatch_nonexistent_driver_returns_400(self):
        data = {"driver": 99999, "transport": self.fx["transport"].pk, "route": self.fx["route"].pk}
        response = self.client.post(self.url_dispatch, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deliver_returns_actual_delivery_date(self):
        self.shipment.status = "in_transit"
        self.shipment.save()
        response = self.client.post(self.url_deliver)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["actual_delivery_date"])

    def test_return_invalid_transition_returns_400(self):
        response = self.client.post(self.url_return)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
