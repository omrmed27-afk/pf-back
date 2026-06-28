from django.db import models
from apps.warehouses.models import Warehouse


class Route(models.Model):
    name = models.CharField(max_length=100)
    origin_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='routes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_order = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    estimated_arrival = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['stop_order']

    def __str__(self):
        return f"{self.route.name} - Parada {self.stop_order}"
