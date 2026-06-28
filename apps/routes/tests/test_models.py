from django.test import TestCase
from django.db.utils import IntegrityError
from apps.routes.models import Route, RouteStop
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="Local Test", address="Calle 1", city="BA", country="AR", capacity=50)


class RouteModelTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Norte", origin_warehouse=self.warehouse)

    def test_create_route(self):
        self.assertEqual(self.route.name, "Ruta Norte")
        self.assertEqual(self.route.origin_warehouse, self.warehouse)

    def test_str_returns_name(self):
        self.assertEqual(str(self.route), "Ruta Norte")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.route.created_at)

    def test_route_protected_from_warehouse_delete(self):
        from django.db.models import ProtectedError
        with self.assertRaises(ProtectedError):
            self.warehouse.delete()


class RouteStopModelTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Sur", origin_warehouse=self.warehouse)
        self.stop = RouteStop.objects.create(
            route=self.route, stop_order=1, address="Calle Entrega 10", city="Buenos Aires"
        )

    def test_create_stop(self):
        self.assertEqual(self.stop.stop_order, 1)
        self.assertEqual(self.stop.city, "Buenos Aires")

    def test_str_returns_route_and_order(self):
        self.assertEqual(str(self.stop), "Ruta Sur - Parada 1")

    def test_estimated_arrival_nullable(self):
        self.assertIsNone(self.stop.estimated_arrival)

    def test_stops_deleted_on_route_delete(self):
        stop_pk = self.stop.pk
        self.route.delete()
        self.assertFalse(RouteStop.objects.filter(pk=stop_pk).exists())

    def test_stops_ordered_by_stop_order(self):
        RouteStop.objects.create(route=self.route, stop_order=3, address="C", city="X")
        RouteStop.objects.create(route=self.route, stop_order=2, address="B", city="X")
        stops = list(RouteStop.objects.filter(route=self.route))
        orders = [s.stop_order for s in stops]
        self.assertEqual(orders, sorted(orders))
