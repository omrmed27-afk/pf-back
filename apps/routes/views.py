from rest_framework.viewsets import ModelViewSet
from .models import Route, RouteStop
from .serializers import RouteSerializer, RouteStopSerializer
from . import services


class RouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer

    def get_queryset(self):
        return services.get_all_routes()


class RouteStopViewSet(ModelViewSet):
    serializer_class = RouteStopSerializer

    def get_queryset(self):
        return RouteStop.objects.all().order_by('route', 'stop_order')
