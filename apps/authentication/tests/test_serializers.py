from django.test import TestCase
from apps.authentication.serializers import LoginSerializer


class LoginSerializerTest(TestCase):

    def test_valid_data_is_valid(self):
        serializer = LoginSerializer(data={"username": "user1", "password": "pass123"})
        self.assertTrue(serializer.is_valid())

    def test_missing_username_is_invalid(self):
        serializer = LoginSerializer(data={"password": "pass123"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_missing_password_is_invalid(self):
        serializer = LoginSerializer(data={"username": "user1"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_password_is_write_only(self):
        serializer = LoginSerializer(data={"username": "user1", "password": "pass123"})
        serializer.is_valid()
        self.assertNotIn("password", serializer.data)
