from rest_framework.viewsets import ModelViewSet
from .models import Transport
from .serializers import TransportSerializer
from . import services


class TransportViewSet(ModelViewSet):
    serializer_class = TransportSerializer

    def get_queryset(self):
        return services.get_all_transports()
