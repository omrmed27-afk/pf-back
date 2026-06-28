from rest_framework.viewsets import ModelViewSet
from .models import Supplier
from .serializers import SupplierSerializer
from . import services


class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        return services.get_all_suppliers()
