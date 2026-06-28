from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Shipment, ShipmentProduct

VALID_TRANSITIONS = {
    Shipment.PENDING: [Shipment.IN_TRANSIT, Shipment.CANCELLED],
    Shipment.IN_TRANSIT: [Shipment.DELIVERED, Shipment.CANCELLED, Shipment.RETURNED],
    Shipment.DELIVERED: [],
    Shipment.CANCELLED: [],
    Shipment.RETURNED: [],
}


def get_all_shipments():
    return Shipment.objects.select_related(
        'customer', 'origin_warehouse', 'driver', 'transport', 'route'
    ).prefetch_related('shipment_products').all().order_by('-created_at')


def get_shipment_by_id(shipment_id):
    return Shipment.objects.select_related(
        'customer', 'origin_warehouse', 'driver', 'transport', 'route'
    ).prefetch_related('shipment_products').get(pk=shipment_id)


def create_shipment(data):
    return Shipment.objects.create(**data)


def update_shipment(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def _change_status(instance, new_status):
    allowed = VALID_TRANSITIONS.get(instance.status, [])
    if new_status not in allowed:
        raise ValidationError(
            f"Transición inválida: {instance.status} → {new_status}. Permitidas: {allowed}"
        )
    instance.status = new_status
    instance.save()
    return instance


@transaction.atomic
def dispatch_shipment(instance, driver, transport, route):
    instance.driver = driver
    instance.transport = transport
    instance.route = route
    return _change_status(instance, Shipment.IN_TRANSIT)


@transaction.atomic
def deliver_shipment(instance):
    instance.actual_delivery_date = timezone.now()
    instance.save()
    return _change_status(instance, Shipment.DELIVERED)


def cancel_shipment(instance):
    return _change_status(instance, Shipment.CANCELLED)


def return_shipment(instance):
    return _change_status(instance, Shipment.RETURNED)


def delete_shipment(instance):
    instance.delete()


def calculate_cost(shipment):
    products = ShipmentProduct.objects.filter(shipment=shipment)
    total = sum(p.quantity * p.unit_price for p in products)
    shipment.calculated_cost = total
    shipment.save()
    return total


@transaction.atomic
def add_product(shipment, product, quantity, unit_price):
    sp = ShipmentProduct.objects.create(
        shipment=shipment, product=product, quantity=quantity, unit_price=unit_price
    )
    calculate_cost(shipment)
    return sp


def remove_product(shipment_product):
    shipment = shipment_product.shipment
    shipment_product.delete()
    calculate_cost(shipment)
