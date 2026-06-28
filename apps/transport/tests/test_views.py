from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.transport.models import Transport

MOCK_TRANSPORT = {
    "license_plate": "VWS001",
    "vehicle_type": "motorcycle",
    "brand": "Yamaha",
    "model": "MT-07",
    "status": "available",
}


class TransportViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.transport = Transport.objects.create(**MOCK_TRANSPORT)
        self.url_list = "/api/v1/transport/"
        self.url_detail = f"/api/v1/transport/{self.transport.id}/"

    # --- Happy path ---

    def test_list_transports(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transport(self):
        data = {"license_plate": "NEW002", "vehicle_type": "van", "status": "available"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["license_plate"], "NEW002")

    def test_retrieve_transport(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["license_plate"], "VWS001")

    def test_update_transport(self):
        data = {**MOCK_TRANSPORT, "status": "maintenance"}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "maintenance")

    def test_partial_update_transport(self):
        response = self.client.patch(self.url_detail, {"status": "in_use"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "in_use")

    def test_delete_transport(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transport.objects.filter(id=self.transport.id).exists())

    # --- Unhappy path ---

    def test_create_without_license_plate_returns_400(self):
        data = {"vehicle_type": "van"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_vehicle_type_returns_400(self):
        data = {"license_plate": "ERR001"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_plate_returns_400(self):
        data = {"license_plate": "VWS001", "vehicle_type": "bicycle"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_vehicle_type_returns_400(self):
        data = {"license_plate": "INV001", "vehicle_type": "truck"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_status_returns_400(self):
        data = {"license_plate": "INV002", "vehicle_type": "van", "status": "broken"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/transport/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Transport.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_ordered_by_license_plate(self):
        Transport.objects.create(license_plate="AAA000", vehicle_type="van")
        Transport.objects.create(license_plate="ZZZ999", vehicle_type="bicycle")
        response = self.client.get(self.url_list)
        plates = [item["license_plate"] for item in response.data["results"]]
        self.assertEqual(plates, sorted(plates))

    def test_all_vehicle_types_accepted(self):
        for plate, vtype in [("M001", "motorcycle"), ("V001", "van"), ("B001", "bicycle")]:
            resp = self.client.post(self.url_list, {"license_plate": plate, "vehicle_type": vtype}, format="json")
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
