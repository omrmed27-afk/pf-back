from django.test import TestCase
from apps.shipments.models import Shipment, ShipmentProduct
from .fixtures import make_all, make_shipment


class ShipmentModelTest(TestCase):

    def setUp(self):
        self.fx = make_all()
        self.shipment = make_shipment(self.fx["customer"], self.fx["warehouse"])

    def test_tracking_number_auto_generated(self):
        self.assertTrue(self.shipment.tracking_number.startswith("SHIP-"))
        self.assertEqual(len(self.shipment.tracking_number), 13)

    def test_tracking_numbers_are_unique(self):
        s2 = make_shipment(self.fx["customer"], self.fx["warehouse"])
        self.assertNotEqual(self.shipment.tracking_number, s2.tracking_number)

    def test_default_status_is_pending(self):
        self.assertEqual(self.shipment.status, "pending")

    def test_default_cost_is_zero(self):
        self.assertEqual(self.shipment.calculated_cost, 0)

    def test_str_contains_tracking_and_status(self):
        self.assertIn(self.shipment.tracking_number, str(self.shipment))
        self.assertIn("pending", str(self.shipment))

    def test_nullable_fields(self):
        self.assertIsNone(self.shipment.driver)
        self.assertIsNone(self.shipment.transport)
        self.assertIsNone(self.shipment.route)
        self.assertIsNone(self.shipment.actual_delivery_date)
        self.assertIsNone(self.shipment.notes)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.shipment.created_at)


class ShipmentProductModelTest(TestCase):

    def setUp(self):
        self.fx = make_all()
        self.shipment = make_shipment(self.fx["customer"], self.fx["warehouse"])
        self.sp = ShipmentProduct.objects.create(
            shipment=self.shipment, product=self.fx["product"], quantity=2, unit_price=10.00
        )

    def test_create_shipment_product(self):
        self.assertEqual(self.sp.quantity, 2)
        self.assertEqual(float(self.sp.unit_price), 10.00)

    def test_str_contains_tracking_and_product(self):
        self.assertIn(self.shipment.tracking_number, str(self.sp))
        self.assertIn("Plato Test", str(self.sp))

    def test_unique_together_shipment_product(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ShipmentProduct.objects.create(
                shipment=self.shipment, product=self.fx["product"], quantity=1, unit_price=5.00
            )

    def test_deleted_on_shipment_delete(self):
        pk = self.sp.pk
        self.shipment.delete()
        self.assertFalse(ShipmentProduct.objects.filter(pk=pk).exists())
