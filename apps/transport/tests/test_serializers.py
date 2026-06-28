from django.test import TestCase
from apps.transport.models import Transport
from apps.transport.serializers import TransportSerializer

MOCK_TRANSPORT = {
    "license_plate": "SER001",
    "vehicle_type": "van",
    "brand": "Ford",
    "model": "Transit",
    "status": "available",
}


class TransportSerializerTest(TestCase):

    def test_valid_data_is_valid(self):
        serializer = TransportSerializer(data=MOCK_TRANSPORT)
        self.assertTrue(serializer.is_valid())

    def test_contains_expected_fields(self):
        transport = Transport.objects.create(**MOCK_TRANSPORT)
        serializer = TransportSerializer(transport)
        fields = set(serializer.data.keys())
        expected = {"id", "license_plate", "vehicle_type", "brand", "model", "status", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_missing_license_plate_is_invalid(self):
        data = {**MOCK_TRANSPORT}
        data.pop("license_plate")
        serializer = TransportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("license_plate", serializer.errors)

    def test_missing_vehicle_type_is_invalid(self):
        data = {**MOCK_TRANSPORT, "license_plate": "SER002"}
        data.pop("vehicle_type")
        serializer = TransportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("vehicle_type", serializer.errors)

    def test_invalid_vehicle_type_is_invalid(self):
        data = {**MOCK_TRANSPORT, "license_plate": "SER003", "vehicle_type": "truck"}
        serializer = TransportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("vehicle_type", serializer.errors)

    def test_invalid_status_is_invalid(self):
        data = {**MOCK_TRANSPORT, "license_plate": "SER004", "status": "broken"}
        serializer = TransportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
