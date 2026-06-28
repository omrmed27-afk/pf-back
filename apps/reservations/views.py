from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError
from .models import Reservation
from .serializers import ReservationSerializer
from . import services


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return services.get_all_reservations()

    def perform_create(self, serializer):
        data = serializer.validated_data
        try:
            reservation = services.create_reservation(data)
            serializer.instance = reservation
        except ValidationError as e:
            from rest_framework.exceptions import ValidationError as DRFValidationError
            raise DRFValidationError({'detail': e.message})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        try:
            updated = services.cancel_reservation(reservation)
            return Response(ReservationSerializer(updated).data)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
