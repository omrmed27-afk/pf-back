import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from apps.customers.models import Customer
from apps.warehouses.models import Warehouse
from apps.suppliers.models import Supplier
from apps.products.models import Product
from apps.drivers.models import Driver
from apps.transport.models import Transport
from apps.routes.models import Route
from apps.shipments.models import Shipment


def make_all():
    warehouse = Warehouse.objects.create(name="Local Test", address="x", city="x", country="x", capacity=10)
    customer = Customer.objects.create(name="Cliente Test", email="ct@ship.com")
    supplier = Supplier.objects.create(name="Prov Test", email="prov@ship.com")
    product = Product.objects.create(name="Plato Test", sku="PLT-001", unit_price=10.00, supplier=supplier)
    user = User.objects.create_user(username="driver_ship", password="pass123", first_name="D", last_name="R")
    driver = Driver.objects.create(user=user, license_number="DRV-001")
    transport = Transport.objects.create(license_plate="TRN-001", vehicle_type="motorcycle")
    route = Route.objects.create(name="Ruta Test", origin_warehouse=warehouse)
    return {
        "warehouse": warehouse,
        "customer": customer,
        "product": product,
        "driver": driver,
        "transport": transport,
        "route": route,
    }


def make_shipment(customer, warehouse):
    return Shipment.objects.create(
        customer=customer,
        origin_warehouse=warehouse,
        destination_address="Calle Entrega 100",
        destination_city="Buenos Aires",
        estimated_delivery_date=timezone.make_aware(datetime.datetime(2026, 8, 1, 18, 0)),
    )
