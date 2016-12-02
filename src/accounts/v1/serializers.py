import json
from rest_framework import serializers

from accounts.models import User
from lib.v1.utils import validate_email as email_is_valid


class LoginRegistrationSerializer(serializers.ModelSerializer):
    facebook_uid = serializers.CharField()
    facebook_access_token = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    branch_data = serializers.JSONField(required=False)

    class Meta:
        model = User
        fields = ('facebook_uid', 'facebook_access_token', 'first_name', 'last_name', 'gender', 'email', 'branch_data',
                  'app_version', 'id')

    def create(self, validated_data):
        """Overriden."""

        defaults = validated_data.copy()
        del defaults['facebook_uid']
        user, created = User.objects.update_or_create(facebook_uid=validated_data['facebook_uid'], defaults=defaults)

        return user

    def validate_email(self, value):
        """
        Email validation.

        :param value: string
        :return: string
        """
        if value and not email_is_valid(value):
            raise serializers.ValidationError('Email is invalid.')

        return value

    def validate_branch_data(self, value):
        """
        Convert branch data to string.

        :param value: dict
        :return: string
        """
        return json.dumps(value)

    def validate_app_version(self, value):
        """
        Validate if version is a float.

        :param value: string
        :return: string
        """
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError('App version not valid.')

        return value


class OneSignalSerializer(serializers.ModelSerializer):
    one_signal_id = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ('one_signal_id',)


class UserEmailUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email',)

    def validate_email(self, value):
        """
        Email validation.

        :param value: string
        :return: string
        """
        if not email_is_valid(value):
            raise serializers.ValidationError('Email is invalid.')

        return value


class UserAppVersionUpdateSerializer(serializers.ModelSerializer):
    app_version = serializers.CharField()

    class Meta:
        model = User
        fields = ('app_version',)

    def validate_app_version(self, value):
        """
        Validate if version is a float.

        :param value: string
        :return: string
        """
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError('App version not valid.')

        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    branch_data = serializers.JSONField(required=False)
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirm_password', 'app_version', 'branch_data')

    def create(self, validated_data):
        """
        Create the object.

        :param validated_data: string
        """
        # remove temporary fields
        del validated_data['name']
        del validated_data['confirm_password']
        # create user and set password
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        """
        Validate if email is valid or there is an user using the email.

        :param value: string
        :return: string
        """

        if not email_is_valid(value):
            raise serializers.ValidationError('Please use a different email address provider.')

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already in use, please use a different email address.')

        return value

    def validate_app_version(self, value):
        """
        Validate if version is a float.

        :param value: string
        :return:
        """
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError('App version not valid.')

        return value

    def validate(self, attrs):
        """
        Generic validate method.

        :param attrs: dict
        :return:
        """
        name_values = attrs['name'].split()
        attrs['first_name'] = name_values[0]
        attrs['last_name'] = ' '.join(name_values[1:]) if len(name_values) > 0 else ''

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(detail='Passwords don\'t match.')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'one_signal_id', 'facebook_access_token', 'facebook_uid',
                  'phone_number')
