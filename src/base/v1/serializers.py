from rest_framework import serializers

from accounts.models import User
from ..models import DiagnosticService


class DiagnosticServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticService
        fields = ('id', 'user', 'vehicle', 'preferred_date', 'time_preference')

