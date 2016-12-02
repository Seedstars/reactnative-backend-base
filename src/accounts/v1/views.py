import json
import shortuuid
import facebook
from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from django_rest_logger import log

import accounts.v1.utils
from accounts.v1.serializers import LoginRegistrationSerializer, OneSignalSerializer, UserRegistrationSerializer, \
    UserSerializer, UserAppVersionUpdateSerializer
from device.models import DeviceOrders
from device.v1.serializers import GetOrderDeviceListSerializer
from lib.v1.exceptions import FacebookInvalidTokenException
from lib.v1.utils import AtomicMixin


class UserLoginRegisterView(GenericAPIView):
    serializer_class = LoginRegistrationSerializer

    def post(self, request):
        """User login view."""
        log.info('UserLoginRegisterView::post::data: {}'.format(json.dumps(request.data)))
        try:
            access_token = request.data['access_token']
            graph_api = facebook.GraphAPI(access_token=access_token, version=settings.FACEBOOK_GRAPH_API_VERSION)
            facebook_user = accounts.v1.utils.get_facebook_user(graph_api)
            long_lived_fb_token = accounts.v1.utils.generate_long_lived_fb_token(access_token, graph_api)
        except KeyError:
            log.warning(message='Authentication failed.', details={'http_status_code': status.HTTP_400_BAD_REQUEST})
            return Response({'access_token': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        except FacebookInvalidTokenException as error:
            log.warning(message='Authentication failed.', details={'http_status_code': status.HTTP_400_BAD_REQUEST})
            return Response({'access_token': [str(error)]}, status=status.HTTP_400_BAD_REQUEST)

        facebook_user['facebook_uid'] = facebook_user.pop('id')
        facebook_user['facebook_access_token'] = long_lived_fb_token
        facebook_user.update(request.data)

        temporary_email = False
        if 'email' not in facebook_user:
            temporary_email = True
            facebook_user['email'] = 'temporary_{}@temporary.com'.format(facebook_user['facebook_uid'])

        serializer = self.get_serializer(data=facebook_user)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        update_last_login(None, user)

        outdated = ('app_version' in request.data and float(request.data['app_version']) < settings.CURRENT_APP_VERSION)

        # create token
        token = AuthToken.objects.create(user)

        email = '' if temporary_email else user.email

        response_data = {
            'token': token,
            'outdated': outdated,
            'user': {
                'id': user.id,
                'one_signal_id': user.one_signal_id,
                'facebook_access_token': user.facebook_access_token,
                'facebook_uid': user.facebook_uid,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': email,
                'phone_number': str(user.phone_number)
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)


class OneSignalView(AtomicMixin, GenericAPIView):
    serializer_class = OneSignalSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Save onSignal id."""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class UserRegisterView(AtomicMixin, CreateModelMixin, GenericAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = ()

    def post(self, request):
        """User registration view."""
        # generate a unique fake facebook_uuid
        request_data = request.data.copy()
        request_data['facebook_uid'] = 'NO_FACE_UUID_{0}'.format(shortuuid.uuid())

        # create the user
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)

        # create authentication token for the user
        token = AuthToken.objects.create(user)

        # check if app version is outdated
        outdated = 'app_version' in request.data and float(request.data['app_version']) < settings.CURRENT_APP_VERSION
        response_data = {
            'token': token,
            'outdated': outdated,
            'user': {
                'id': user.id,
                'one_signal_id': user.one_signal_id,
                'facebook_access_token': user.facebook_access_token,
                'facebook_uid': user.facebook_uid,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': str(user.phone_number)
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """User login view with username and password."""
        try:
            outdated = 'app_version' in request.data and float(
                request.data['app_version']) < settings.CURRENT_APP_VERSION
        except ValueError:
            return Response({'app_version': ['App version not valid.']}, status=status.HTTP_400_BAD_REQUEST)

        token = AuthToken.objects.create(request.user)
        user = self.get_serializer(request.user).data

        if 'app_version' in request.data:
            serializer = UserAppVersionUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user, serializer.validated_data)
        device_orders = DeviceOrders.objects.filter(user=request.user)
        user['device'] = GetOrderDeviceListSerializer(device_orders, many=True).data if device_orders else None

        response_data = {
            'token': token,
            'outdated': outdated,
            'user': user
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UserLogoutView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """User logout."""

        request._auth.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
