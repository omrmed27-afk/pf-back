from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from apps.drivers.models import Driver


def make_user(username="driver1", first_name="Juan", last_name="Pérez"):
    return User.objects.create_user(username=username, password="pass123", first_name=first_name, last_name=last_name)


class DriverModelTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.driver = Driver.objects.create(user=self.user, license_number="LIC-001", phone="1234567890")

    def test_create_driver(self):
        self.assertEqual(self.driver.license_number, "LIC-001")
        self.assertEqual(self.driver.user, self.user)

    def test_str_returns_fullname_and_license(self):
        self.assertEqual(str(self.driver), "Juan Pérez (LIC-001)")

    def test_default_status_is_available(self):
        self.assertEqual(self.driver.status, "available")

    def test_license_number_is_unique(self):
        user2 = make_user(username="driver2")
        with self.assertRaises(IntegrityError):
            Driver.objects.create(user=user2, license_number="LIC-001")

    def test_user_is_onetoone(self):
        user2 = make_user(username="driver3")
        driver2 = Driver.objects.create(user=user2, license_number="LIC-002")
        self.assertEqual(user2.driver, driver2)

    def test_driver_deleted_on_user_delete(self):
        driver_pk = self.driver.pk
        self.user.delete()
        self.assertFalse(Driver.objects.filter(pk=driver_pk).exists())

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.driver.created_at)
