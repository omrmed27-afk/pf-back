from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class LoginViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="login_user", password="correct_pass")
        self.url = "/api/v1/auth/login/"

    # --- Happy path ---

    def test_login_valid_credentials_returns_token(self):
        response = self.client.post(self.url, {"username": "login_user", "password": "correct_pass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_creates_token_in_db(self):
        self.client.post(self.url, {"username": "login_user", "password": "correct_pass"}, format="json")
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    # --- Unhappy path ---

    def test_login_wrong_password_returns_401(self):
        response = self.client.post(self.url, {"username": "login_user", "password": "wrong"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_username_returns_400(self):
        response = self.client.post(self.url, {"password": "correct_pass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password_returns_400(self):
        response = self.client.post(self.url, {"username": "login_user"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user_returns_401(self):
        response = self.client.post(self.url, {"username": "nadie", "password": "pass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_login_empty_body_returns_400(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_idempotent_same_token(self):
        r1 = self.client.post(self.url, {"username": "login_user", "password": "correct_pass"}, format="json")
        r2 = self.client.post(self.url, {"username": "login_user", "password": "correct_pass"}, format="json")
        self.assertEqual(r1.data["token"], r2.data["token"])


class LogoutViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="logout_user", password="pass123")
        self.token = Token.objects.create(user=self.user)
        self.url = "/api/v1/auth/logout/"

    # --- Happy path ---

    def test_logout_authenticated_returns_204(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_deletes_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.client.post(self.url)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_token_invalid_after_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.client.post(self.url)
        response = self.client.get("/api/v1/warehouses/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Unhappy path ---

    def test_logout_unauthenticated_returns_401(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterDriverViewTest(APITestCase):

    def setUp(self):
        self.url = "/api/v1/auth/register/"

    def test_register_valid_driver_returns_201(self):
        data = {"username": "nuevo_rep", "password": "pass123", "license_number": "LIC-REG-001"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("license_number", response.data)

    def test_register_creates_user_and_driver(self):
        data = {"username": "rep2", "password": "pass123", "license_number": "LIC-REG-002",
                "first_name": "Ana", "last_name": "López"}
        self.client.post(self.url, data, format="json")
        from django.contrib.auth.models import User
        from apps.drivers.models import Driver
        self.assertTrue(User.objects.filter(username="rep2").exists())
        self.assertTrue(Driver.objects.filter(license_number="LIC-REG-002").exists())

    def test_register_missing_license_returns_400(self):
        data = {"username": "rep3", "password": "pass123"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username_returns_400(self):
        data = {"username": "rep_dup", "password": "pass123", "license_number": "LIC-REG-003"}
        self.client.post(self.url, data, format="json")
        data2 = {"username": "rep_dup", "password": "pass123", "license_number": "LIC-REG-004"}
        response = self.client.post(self.url, data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_license_returns_400(self):
        data = {"username": "rep_a", "password": "pass123", "license_number": "LIC-DUP"}
        self.client.post(self.url, data, format="json")
        data2 = {"username": "rep_b", "password": "pass123", "license_number": "LIC-DUP"}
        response = self.client.post(self.url, data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
