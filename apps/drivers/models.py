from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    AVAILABLE = 'available'
    ON_ROUTE = 'on_route'
    OFF_DUTY = 'off_duty'
    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (ON_ROUTE, 'En ruta'),
        (OFF_DUTY, 'Fuera de servicio'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    license_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.license_number})"
