from rest_framework import serializers

from accounts.models import User

from lib.utils import validate_email as email_is_valid


class LoginRegistrationSerializer(serializers.Serializer):
    facebook_uid = serializers.CharField()
    facebook_access_token = serializers.CharField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def create(self, validated_data):
        """Overriden."""
        defaults = validated_data.copy()
        del defaults['facebook_uid']
        user, _ = User.objects.update_or_create(
            facebook_uid=validated_data['facebook_uid'],
            defaults=defaults
        )
        return user

    def update(self, instance, validated_data):  # pragma: no cover
        """Overriden."""
        pass

    def validate_email(self, value):
        """Email validation."""
        if value and not email_is_valid(value):
            raise serializers.ValidationError('Email is invalid.')

        return value
        
class OneSignalSerializer(serializers.ModelSerializer):
    one_signal_id = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ('one_signal_id',)
