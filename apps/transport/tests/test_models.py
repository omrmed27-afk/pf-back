from django.test import TestCase
from django.db import IntegrityError
from apps.transport.models import Transport

MOCK_TRANSPORT = {
    "license_plate": "ABC123",
    "vehicle_type": "motorcycle",
    "brand": "Honda",
    "model": "CB500",
    "status": "available",
}


class TransportModelTest(TestCase):

    def setUp(self):
        self.transport = Transport.objects.create(**MOCK_TRANSPORT)

    def test_create_transport(self):
        self.assertEqual(self.transport.license_plate, "ABC123")
        self.assertEqual(self.transport.vehicle_type, "motorcycle")
        self.assertEqual(self.transport.status, "available")

    def test_str_returns_plate_and_type(self):
        self.assertEqual(str(self.transport), "ABC123 (motorcycle)")

    def test_license_plate_is_unique(self):
        with self.assertRaises(IntegrityError):
            Transport.objects.create(license_plate="ABC123", vehicle_type="van")

    def test_default_status_is_available(self):
        transport = Transport.objects.create(license_plate="XYZ999", vehicle_type="bicycle")
        self.assertEqual(transport.status, "available")

    def test_optional_fields_can_be_empty(self):
        transport = Transport.objects.create(license_plate="MIN001", vehicle_type="van")
        self.assertEqual(transport.brand, "")
        self.assertEqual(transport.model, "")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.transport.created_at)
