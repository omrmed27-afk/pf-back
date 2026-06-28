from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from apps.routes.models import Route, RouteStop
from apps.warehouses.models import Warehouse


def make_warehouse():
    return Warehouse.objects.create(name="WH Views", address="x", city="x", country="x", capacity=10)


class RouteViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Views", origin_warehouse=self.warehouse)
        self.url_list = "/api/v1/routes/"
        self.url_detail = f"/api/v1/routes/{self.route.id}/"

    # --- Happy path ---

    def test_list_routes(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_route(self):
        data = {"name": "Ruta Nueva", "origin_warehouse": self.warehouse.pk}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Ruta Nueva")

    def test_retrieve_route(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Ruta Views")

    def test_retrieve_route_has_stops(self):
        RouteStop.objects.create(route=self.route, stop_order=1, address="Calle A", city="BA")
        response = self.client.get(self.url_detail)
        self.assertIn("stops", response.data)
        self.assertEqual(len(response.data["stops"]), 1)

    def test_update_route(self):
        data = {"name": "Ruta Editada", "origin_warehouse": self.warehouse.pk}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Ruta Editada")

    def test_partial_update_route(self):
        response = self.client.patch(self.url_detail, {"name": "Parcial"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Parcial")

    def test_delete_route(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Route.objects.filter(id=self.route.id).exists())

    # --- Unhappy path ---

    def test_create_without_name_returns_400(self):
        response = self.client.post(self.url_list, {"origin_warehouse": self.warehouse.pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_warehouse_returns_400(self):
        response = self.client.post(self.url_list, {"name": "Sin Almacen"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/routes/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Edge cases ---

    def test_list_empty_returns_200(self):
        Route.objects.all().delete()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RouteStopViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="stop_user", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.warehouse = make_warehouse()
        self.route = Route.objects.create(name="Ruta Stops", origin_warehouse=self.warehouse)
        self.stop = RouteStop.objects.create(route=self.route, stop_order=1, address="Av. Test 1", city="BA")
        self.url_list = "/api/v1/route-stops/"
        self.url_detail = f"/api/v1/route-stops/{self.stop.id}/"

    def test_list_stops(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_stop(self):
        data = {"route": self.route.pk, "stop_order": 2, "address": "Calle Nueva 99", "city": "Rosario"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["stop_order"], 2)

    def test_retrieve_stop(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "BA")

    def test_update_stop(self):
        data = {"route": self.route.pk, "stop_order": 1, "address": "Av. Test 1", "city": "Córdoba"}
        response = self.client.put(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "Córdoba")

    def test_delete_stop(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RouteStop.objects.filter(id=self.stop.id).exists())

    def test_create_stop_without_address_returns_400(self):
        data = {"route": self.route.pk, "stop_order": 3, "city": "BA"}
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stop_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/route-stops/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
