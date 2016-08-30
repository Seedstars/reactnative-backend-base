from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError
from rest_framework import serializers

from device.models import DeviceOrders


class OrderDeviceSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True)

    class Meta:
        model = DeviceOrders
        fields = ('id', 'user', 'address', 'phone_number', 'payment')

    def validate_phone_number(self, value):
        """Tracker phone number validation."""
        try:
            validate_international_phonenumber(value)
        except ValidationError:
            raise serializers.ValidationError('Phone number is not valid.')
        return value


class GetOrderDeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceOrders
        fields = ('id', 'user', 'address', 'phone_number', 'payment', 'paid')

    def to_representation(self, instance):
        """Representation of OrderDevice."""

        data = {
            'id': instance.id,
            'user': instance.user.id,
            'address': instance.address,
            'phone_number': instance.phone_number,
            'payment': instance.get_payment_display(),
            'paid': instance.get_paid_display(),
        }
        return data
