from django.db import models
from apps.customers.models import Customer
from apps.tables.models import Table


class Reservation(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (CONFIRMED, 'Confirmada'),
        (CANCELLED, 'Cancelada'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    party_size = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - Mesa {self.table.number} ({self.date})"
