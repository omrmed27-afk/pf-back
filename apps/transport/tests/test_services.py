from django.test import TestCase
from apps.transport.models import Transport
from apps.transport import services

MOCK_TRANSPORT = {
    "license_plate": "SVC001",
    "vehicle_type": "motorcycle",
    "status": "available",
}


class TransportServicesTest(TestCase):

    def setUp(self):
        self.transport = Transport.objects.create(**MOCK_TRANSPORT)

    def test_get_all_transports_returns_queryset(self):
        result = services.get_all_transports()
        self.assertIn(self.transport, result)

    def test_get_all_transports_ordered_by_license_plate(self):
        Transport.objects.create(license_plate="AAA000", vehicle_type="van")
        Transport.objects.create(license_plate="ZZZ999", vehicle_type="bicycle")
        result = list(services.get_all_transports())
        plates = [t.license_plate for t in result]
        self.assertEqual(plates, sorted(plates))

    def test_get_transport_by_id(self):
        result = services.get_transport_by_id(self.transport.pk)
        self.assertEqual(result, self.transport)

    def test_get_transport_by_id_raises_on_missing(self):
        with self.assertRaises(Transport.DoesNotExist):
            services.get_transport_by_id(99999)

    def test_create_transport(self):
        data = {"license_plate": "NEW001", "vehicle_type": "bicycle"}
        transport = services.create_transport(data)
        self.assertTrue(Transport.objects.filter(pk=transport.pk).exists())

    def test_update_transport(self):
        updated = services.update_transport(self.transport, {"status": "in_use"})
        self.assertEqual(updated.status, "in_use")
        self.transport.refresh_from_db()
        self.assertEqual(self.transport.status, "in_use")

    def test_delete_transport(self):
        pk = self.transport.pk
        services.delete_transport(self.transport)
        self.assertFalse(Transport.objects.filter(pk=pk).exists())
