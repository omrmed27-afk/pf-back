from django.test import TestCase
from django.contrib.auth.models import User
from apps.drivers.models import Driver
from apps.drivers import services


class DriverServicesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="svc_driver", password="pass123",
                                             first_name="Carlos", last_name="Ruiz")
        self.driver = Driver.objects.create(user=self.user, license_number="SVC-001", status="available")

    def test_get_all_drivers_returns_queryset(self):
        result = services.get_all_drivers()
        self.assertIn(self.driver, result)

    def test_get_driver_by_id(self):
        result = services.get_driver_by_id(self.driver.pk)
        self.assertEqual(result, self.driver)

    def test_get_driver_by_id_raises_on_missing(self):
        with self.assertRaises(Driver.DoesNotExist):
            services.get_driver_by_id(99999)

    def test_create_driver_with_user(self):
        user_data = {"username": "nuevo_driver", "password": "pass123",
                     "first_name": "Nuevo", "last_name": "Driver"}
        driver_data = {"license_number": "NUE-001", "phone": "9876543210"}
        driver = services.create_driver_with_user(user_data, driver_data)
        self.assertIsNotNone(driver.pk)
        self.assertTrue(User.objects.filter(username="nuevo_driver").exists())

    def test_create_driver_with_user_is_atomic(self):
        user_data = {"username": "atomic_driver", "password": "pass123"}
        driver_data = {"license_number": "SVC-001"}  # duplicate — should rollback
        with self.assertRaises(Exception):
            services.create_driver_with_user(user_data, driver_data)
        self.assertFalse(User.objects.filter(username="atomic_driver").exists())

    def test_update_driver(self):
        updated = services.update_driver(self.driver, {"status": "on_route"})
        self.assertEqual(updated.status, "on_route")
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.status, "on_route")

    def test_delete_driver(self):
        pk = self.driver.pk
        services.delete_driver(self.driver)
        self.assertFalse(Driver.objects.filter(pk=pk).exists())
