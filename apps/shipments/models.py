import uuid
from django.db import models
from apps.customers.models import Customer
from apps.warehouses.models import Warehouse
from apps.drivers.models import Driver
from apps.transport.models import Transport
from apps.routes.models import Route
from apps.products.models import Product


class Shipment(models.Model):
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'
    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (IN_TRANSIT, 'En tránsito'),
        (DELIVERED, 'Entregado'),
        (CANCELLED, 'Cancelado'),
        (RETURNED, 'Devuelto'),
    ]

    tracking_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='shipments')
    origin_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='shipments')
    destination_address = models.TextField()
    destination_city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    estimated_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    calculated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = f"SHIP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_number} ({self.status})"


class ShipmentProduct(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='shipment_products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='shipment_products')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [('shipment', 'product')]

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.product.name} x{self.quantity}"
