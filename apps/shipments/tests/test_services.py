from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.shipments.models import Shipment, ShipmentProduct
from apps.shipments import services
from .fixtures import make_all, make_shipment


class ShipmentServicesTest(TestCase):

    def setUp(self):
        self.fx = make_all()
        self.shipment = make_shipment(self.fx["customer"], self.fx["warehouse"])

    def test_get_all_shipments(self):
        result = services.get_all_shipments()
        self.assertIn(self.shipment, result)

    def test_get_shipment_by_id(self):
        result = services.get_shipment_by_id(self.shipment.pk)
        self.assertEqual(result, self.shipment)

    def test_get_shipment_by_id_raises_on_missing(self):
        with self.assertRaises(Shipment.DoesNotExist):
            services.get_shipment_by_id(99999)

    def test_update_shipment(self):
        updated = services.update_shipment(self.shipment, {"destination_city": "Rosario"})
        self.assertEqual(updated.destination_city, "Rosario")

    def test_delete_shipment(self):
        pk = self.shipment.pk
        services.delete_shipment(self.shipment)
        self.assertFalse(Shipment.objects.filter(pk=pk).exists())

    # --- Status transitions ---

    def test_dispatch_pending_to_in_transit(self):
        updated = services.dispatch_shipment(
            self.shipment, self.fx["driver"], self.fx["transport"], self.fx["route"]
        )
        self.assertEqual(updated.status, "in_transit")
        self.assertEqual(updated.driver, self.fx["driver"])

    def test_dispatch_non_pending_raises(self):
        self.shipment.status = "delivered"
        self.shipment.save()
        with self.assertRaises(ValidationError):
            services.dispatch_shipment(
                self.shipment, self.fx["driver"], self.fx["transport"], self.fx["route"]
            )

    def test_deliver_in_transit(self):
        services.dispatch_shipment(
            self.shipment, self.fx["driver"], self.fx["transport"], self.fx["route"]
        )
        updated = services.deliver_shipment(self.shipment)
        self.assertEqual(updated.status, "delivered")
        self.assertIsNotNone(updated.actual_delivery_date)

    def test_deliver_non_in_transit_raises(self):
        with self.assertRaises(ValidationError):
            services.deliver_shipment(self.shipment)

    def test_cancel_pending(self):
        updated = services.cancel_shipment(self.shipment)
        self.assertEqual(updated.status, "cancelled")

    def test_cancel_in_transit(self):
        services.dispatch_shipment(
            self.shipment, self.fx["driver"], self.fx["transport"], self.fx["route"]
        )
        updated = services.cancel_shipment(self.shipment)
        self.assertEqual(updated.status, "cancelled")

    def test_cancel_delivered_raises(self):
        self.shipment.status = "delivered"
        self.shipment.save()
        with self.assertRaises(ValidationError):
            services.cancel_shipment(self.shipment)

    def test_return_in_transit(self):
        services.dispatch_shipment(
            self.shipment, self.fx["driver"], self.fx["transport"], self.fx["route"]
        )
        updated = services.return_shipment(self.shipment)
        self.assertEqual(updated.status, "returned")

    # --- Products y costos ---

    def test_add_product_creates_shipment_product(self):
        sp = services.add_product(self.shipment, self.fx["product"], quantity=2, unit_price=10.00)
        self.assertIsNotNone(sp.pk)

    def test_add_product_recalculates_cost(self):
        services.add_product(self.shipment, self.fx["product"], quantity=3, unit_price=10.00)
        self.shipment.refresh_from_db()
        self.assertEqual(float(self.shipment.calculated_cost), 30.00)

    def test_calculate_cost_multiple_products(self):
        from apps.products.models import Product
        p2 = Product.objects.create(name="Plato 2", sku="PLT-002", unit_price=5.00)
        services.add_product(self.shipment, self.fx["product"], quantity=2, unit_price=10.00)
        services.add_product(self.shipment, p2, quantity=4, unit_price=5.00)
        self.shipment.refresh_from_db()
        self.assertEqual(float(self.shipment.calculated_cost), 40.00)

    def test_remove_product_recalculates_cost(self):
        sp = services.add_product(self.shipment, self.fx["product"], quantity=2, unit_price=10.00)
        services.remove_product(sp)
        self.shipment.refresh_from_db()
        self.assertEqual(float(self.shipment.calculated_cost), 0.00)
