from django.db import models
from apps.warehouses.models import Warehouse


class Table(models.Model):
    AVAILABLE = 'available'
    RESERVED = 'reserved'
    OCCUPIED = 'occupied'
    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (RESERVED, 'Reservada'),
        (OCCUPIED, 'Ocupada'),
    ]

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='tables')
    number = models.IntegerField()
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('warehouse', 'number')]

    def __str__(self):
        return f"Mesa {self.number} - {self.warehouse.name}"
