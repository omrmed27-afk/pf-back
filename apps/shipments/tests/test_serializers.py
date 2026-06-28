import datetime
from django.test import TestCase
from apps.shipments.serializers import ShipmentSerializer, ShipmentProductSerializer
from apps.shipments.models import ShipmentProduct
from .fixtures import make_all, make_shipment


class ShipmentSerializerTest(TestCase):

    def setUp(self):
        self.fx = make_all()
        self.shipment = make_shipment(self.fx["customer"], self.fx["warehouse"])

    def test_contains_expected_fields(self):
        serializer = ShipmentSerializer(self.shipment)
        expected = {
            "id", "tracking_number", "customer", "origin_warehouse",
            "destination_address", "destination_city", "status",
            "estimated_delivery_date", "actual_delivery_date", "calculated_cost",
            "driver", "transport", "route", "notes", "shipment_products",
            "created_at", "updated_at"
        }
        self.assertEqual(set(serializer.data.keys()), expected)

    def test_tracking_number_read_only(self):
        data = {
            "customer": self.fx["customer"].pk,
            "origin_warehouse": self.fx["warehouse"].pk,
            "destination_address": "Calle X",
            "destination_city": "BA",
            "estimated_delivery_date": "2026-09-01T18:00:00Z",
            "tracking_number": "MANUAL-001",
        }
        serializer = ShipmentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertNotEqual(instance.tracking_number, "MANUAL-001")

    def test_missing_customer_is_invalid(self):
        data = {
            "origin_warehouse": self.fx["warehouse"].pk,
            "destination_address": "x", "destination_city": "x",
            "estimated_delivery_date": "2026-09-01T18:00:00Z",
        }
        serializer = ShipmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)

    def test_shipment_products_nested_read(self):
        ShipmentProduct.objects.create(
            shipment=self.shipment, product=self.fx["product"], quantity=1, unit_price=10.00
        )
        serializer = ShipmentSerializer(self.shipment)
        self.assertEqual(len(serializer.data["shipment_products"]), 1)


class ShipmentProductSerializerTest(TestCase):

    def setUp(self):
        self.fx = make_all()
        self.shipment = make_shipment(self.fx["customer"], self.fx["warehouse"])

    def test_valid_data_is_valid(self):
        data = {
            "shipment": self.shipment.pk,
            "product": self.fx["product"].pk,
            "quantity": 3,
            "unit_price": "12.50",
        }
        serializer = ShipmentProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_quantity_is_invalid(self):
        data = {"shipment": self.shipment.pk, "product": self.fx["product"].pk, "unit_price": "5.00"}
        serializer = ShipmentProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)
