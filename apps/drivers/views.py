from rest_framework.viewsets import ModelViewSet
from .models import Driver
from .serializers import DriverSerializer
from . import services


class DriverViewSet(ModelViewSet):
    serializer_class = DriverSerializer

    def get_queryset(self):
        return services.get_all_drivers()
