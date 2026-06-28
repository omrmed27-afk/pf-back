from django.db import models


class Transport(models.Model):
    MOTORCYCLE = 'motorcycle'
    VAN = 'van'
    BICYCLE = 'bicycle'
    VEHICLE_TYPE_CHOICES = [
        (MOTORCYCLE, 'Moto'),
        (VAN, 'Furgoneta'),
        (BICYCLE, 'Bicicleta'),
    ]

    AVAILABLE = 'available'
    IN_USE = 'in_use'
    MAINTENANCE = 'maintenance'
    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (IN_USE, 'En uso'),
        (MAINTENANCE, 'En mantenimiento'),
    ]

    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    brand = models.CharField(max_length=100, blank=True, default='')
    model = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.license_plate} ({self.vehicle_type})"
