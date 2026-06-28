from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import ValidationError
from .models import Table
from .serializers import TableSerializer
from . import services


class TableViewSet(ModelViewSet):
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        qs = services.get_all_tables()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        capacity = self.request.query_params.get('min_capacity')
        if capacity:
            qs = qs.filter(capacity__gte=int(capacity))
        return qs

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        table = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'detail': 'Campo status requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = services.change_status(table, new_status)
            return Response(TableSerializer(updated).data)
        except ValidationError as e:
            return Response({'detail': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
