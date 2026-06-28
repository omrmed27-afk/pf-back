from rest_framework.viewsets import ModelViewSet
from .models import Warehouse
from .serializers import WarehouseSerializer


class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all().order_by('name')
    serializer_class = WarehouseSerializer
