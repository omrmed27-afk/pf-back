from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.drivers.models import Driver


def make_driver_user(username="driver_view", license_number="VWS-001"):
    user = User.objects.create_user(username=username, password="pass123",
                                    first_name="Pedro", last_name="Soto")
    driver = Driver.objects.create(user=user, license_number=license_number, status="available")
    return user, driver


class DriverViewSetTest(APITestCase):

    def setUp(self):
        self.auth_user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.driver_user, self.driver = make_driver_user()
        self.url_list = "/api/v1/drivers/"
        self.url_detail = f"/api/v1/drivers/{self.driver.id}/"

    # --- Happy path ---

    def test_list_drivers(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_driver(self):
        new_user = User.objects.create_user(username="new_driver_user", password="pass123")
        data = {"user_id": new_user.pk, "license_number": "NEW-001", "status": "available"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["license_number"], "NEW-001")

    def test_retrieve_driver(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["license_number"], "VWS-001")

    def test_retrieve_driver_has_nested_user(self):
        response = self.client.get(self.url_detail)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "driver_view")

    def test_update_driver_status(self):
        data = {"user_id": self.driver_user.pk, "license_number": "VWS-001", "status": "on_route"}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "on_route")

    def test_partial_update_driver(self):
        response = self.client.patch(self.url_detail, {"status": "off_duty"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "off_duty")

    def test_delete_driver(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())

    # --- Unhappy path ---

    def test_create_without_license_returns_400(self):
        new_user = User.objects.create_user(username="no_lic_user", password="pass123")
        data = {"user_id": new_user.pk, "status": "available"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_user_returns_400(self):
        data = {"license_number": "ERR-001", "status": "available"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_license_returns_400(self):
        new_user = User.objects.create_user(username="dup_user", password="pass123")
        data = {"user_id": new_user.pk, "license_number": "VWS-001"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_status_returns_400(self):
        new_user = User.objects.create_user(username="inv_status_user", password="pass123")
        data = {"user_id": new_user.pk, "license_number": "INV-001", "status": "volando"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/drivers/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Driver.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_statuses_accepted(self):
        users = [User.objects.create_user(username=f"s_user_{i}", password="pass") for i in range(3)]
        for i, (user, st) in enumerate(zip(users, ["available", "on_route", "off_duty"])):
            resp = self.client.post(self.url_list,
                                    {"user_id": user.pk, "license_number": f"ST-00{i}", "status": st},
                                    format="json")
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
