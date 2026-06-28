from django.test import TestCase
from apps.routes.models import Route, RouteStop
from apps.routes.serializers import RouteSerializer, RouteStopSerializer
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="WH Ser", address="x", city="x", country="x", capacity=10)


class RouteSerializerTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Ser", origin_warehouse=self.warehouse)

    def test_valid_data_is_valid(self):
        data = {"name": "Nueva Ruta", "origin_warehouse": self.warehouse.pk}
        serializer = RouteSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contains_expected_fields(self):
        serializer = RouteSerializer(self.route)
        fields = set(serializer.data.keys())
        expected = {"id", "name", "origin_warehouse", "stops", "created_at", "updated_at"}
        self.assertEqual(fields, expected)

    def test_stops_nested_in_response(self):
        RouteStop.objects.create(route=self.route, stop_order=1, address="Calle A", city="BA")
        serializer = RouteSerializer(self.route)
        self.assertEqual(len(serializer.data["stops"]), 1)

    def test_missing_name_is_invalid(self):
        data = {"origin_warehouse": self.warehouse.pk}
        serializer = RouteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_warehouse_is_invalid(self):
        data = {"name": "Sin Almacen"}
        serializer = RouteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("origin_warehouse", serializer.errors)


class RouteStopSerializerTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Stop", origin_warehouse=self.warehouse)

    def test_valid_stop_data_is_valid(self):
        data = {"route": self.route.pk, "stop_order": 1, "address": "Calle X 100", "city": "Rosario"}
        serializer = RouteStopSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_address_is_invalid(self):
        data = {"route": self.route.pk, "stop_order": 1, "city": "Rosario"}
        serializer = RouteStopSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("address", serializer.errors)

    def test_estimated_arrival_optional(self):
        data = {"route": self.route.pk, "stop_order": 1, "address": "x", "city": "x", "estimated_arrival": None}
        serializer = RouteStopSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
