from django.test import TestCase
from django.contrib.auth.models import User
from apps.drivers.models import Driver
from apps.drivers.serializers import DriverSerializer


def make_user(username="ser_driver"):
    return User.objects.create_user(username=username, password="pass123", first_name="Ana", last_name="Gómez")


class DriverSerializerTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.driver = Driver.objects.create(user=self.user, license_number="SER-001", status="available")

    def test_contains_expected_fields(self):
        serializer = DriverSerializer(self.driver)
        fields = set(serializer.data.keys())
        # user_id es write_only, no aparece en la respuesta
        expected = {"id", "user", "license_number", "phone", "status", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_user_nested_in_read(self):
        serializer = DriverSerializer(self.driver)
        self.assertIn("username", serializer.data["user"])
        self.assertEqual(serializer.data["user"]["username"], "ser_driver")

    def test_valid_write_data(self):
        user2 = make_user(username="ser_driver2")
        data = {"user_id": user2.pk, "license_number": "SER-002", "status": "available"}
        serializer = DriverSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_license_number_is_invalid(self):
        user2 = make_user(username="ser_driver3")
        data = {"user_id": user2.pk, "status": "available"}
        serializer = DriverSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("license_number", serializer.errors)

    def test_missing_user_id_is_invalid(self):
        data = {"license_number": "SER-003", "status": "available"}
        serializer = DriverSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user_id", serializer.errors)

    def test_invalid_status_is_invalid(self):
        user2 = make_user(username="ser_driver4")
        data = {"user_id": user2.pk, "license_number": "SER-004", "status": "inexistente"}
        serializer = DriverSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
