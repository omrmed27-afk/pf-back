from rest_framework import serializers
from .models import Shipment, ShipmentProduct


class ShipmentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentProduct
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    shipment_products = ShipmentProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields = ['tracking_number', 'actual_delivery_date']
