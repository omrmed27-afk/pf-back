from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Shipment, ShipmentProduct
from .serializers import ShipmentSerializer, ShipmentProductSerializer
from . import services


class ShipmentViewSet(ModelViewSet):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return services.get_all_shipments()

    @action(detail=True, methods=['post'], url_path='dispatch')
    def dispatch_shipment(self, request, pk=None):
        shipment = self.get_object()
        driver_id = request.data.get('driver')
        transport_id = request.data.get('transport')
        route_id = request.data.get('route')
        if not all([driver_id, transport_id, route_id]):
            return Response(
                {'detail': 'Se requieren driver, transport y route.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        from apps.drivers.models import Driver
        from apps.transport.models import Transport
        from apps.routes.models import Route
        try:
            driver = Driver.objects.get(pk=driver_id)
            transport = Transport.objects.get(pk=transport_id)
            route = Route.objects.get(pk=route_id)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = services.dispatch_shipment(shipment, driver, transport, route)
            return Response(ShipmentSerializer(updated).data)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='deliver')
    def deliver(self, request, pk=None):
        shipment = self.get_object()
        try:
            updated = services.deliver_shipment(shipment)
            return Response(ShipmentSerializer(updated).data)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        shipment = self.get_object()
        try:
            updated = services.cancel_shipment(shipment)
            return Response(ShipmentSerializer(updated).data)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='return')
    def return_shipment(self, request, pk=None):
        shipment = self.get_object()
        try:
            updated = services.return_shipment(shipment)
            return Response(ShipmentSerializer(updated).data)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)


class ShipmentProductViewSet(ModelViewSet):
    serializer_class = ShipmentProductSerializer

    def get_queryset(self):
        return ShipmentProduct.objects.select_related('shipment', 'product').all()
