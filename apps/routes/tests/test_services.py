from django.test import TestCase
from apps.routes.models import Route, RouteStop
from apps.routes import services
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="WH Svc", address="x", city="x", country="x", capacity=10)


class RouteServicesTest(TestCase):

    def setUp(self):
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Svc", origin_warehouse=self.warehouse)
        self.stop = RouteStop.objects.create(route=self.route, stop_order=1, address="Av A 10", city="BA")

    def test_get_all_routes(self):
        result = services.get_all_routes()
        self.assertIn(self.route, result)

    def test_get_route_by_id(self):
        result = services.get_route_by_id(self.route.pk)
        self.assertEqual(result, self.route)

    def test_get_route_by_id_raises_on_missing(self):
        with self.assertRaises(Route.DoesNotExist):
            services.get_route_by_id(99999)

    def test_create_route(self):
        route = services.create_route({"name": "Nueva", "origin_warehouse": self.warehouse})
        self.assertTrue(Route.objects.filter(pk=route.pk).exists())

    def test_update_route(self):
        updated = services.update_route(self.route, {"name": "Actualizada"})
        self.assertEqual(updated.name, "Actualizada")

    def test_delete_route(self):
        pk = self.route.pk
        services.delete_route(self.route)
        self.assertFalse(Route.objects.filter(pk=pk).exists())

    def test_get_all_stops(self):
        result = services.get_all_stops(self.route.pk)
        self.assertIn(self.stop, result)

    def test_create_stop(self):
        stop = services.create_stop({"route": self.route, "stop_order": 2, "address": "Calle B", "city": "ROS"})
        self.assertTrue(RouteStop.objects.filter(pk=stop.pk).exists())

    def test_update_stop(self):
        updated = services.update_stop(self.stop, {"city": "Córdoba"})
        self.assertEqual(updated.city, "Córdoba")

    def test_delete_stop(self):
        pk = self.stop.pk
        services.delete_stop(self.stop)
        self.assertFalse(RouteStop.objects.filter(pk=pk).exists())
