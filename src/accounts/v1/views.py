import json

import accounts.v1.utils
import facebook
from accounts.v1.exceptions import FacebookInvalidTokenException
from django.conf import settings
from django_rest_logger import log
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from accounts.v1.serializers import LoginRegistrationSerializer, OneSignalSerializer

from lib.utils import AtomicMixin

class UserLoginRegisterView(APIView):
    serializer_class = LoginRegistrationSerializer

    def post(self, request):
        """
        User login view.

        Based on JSONWebTokenAPIView from rest_framework_jwt.
        """

        log.info('UserLoginRegisterView::post::data: {}'.format(json.dumps(request.data)))
        try:
            access_token = request.data['access_token']
            graph_api = facebook.GraphAPI(access_token=access_token, version=settings.FACEBOOK_GRAPH_API_VERSION)

            facebook_user = accounts.v1.utils.get_facebook_user(graph_api)
            long_lived_fb_token = accounts.v1.utils.generate_long_lived_fb_token(access_token, graph_api)

        except KeyError:
            log.warning(message='Authentication failed.', details={'http_status_code': status.HTTP_400_BAD_REQUEST})
            return Response({'access_token': ['This field is required']}, status=status.HTTP_400_BAD_REQUEST)
        except FacebookInvalidTokenException as error:
            log.warning(message='Authentication failed.', details={'http_status_code': status.HTTP_400_BAD_REQUEST})
            return Response({'access_token': [str(error)]}, status=status.HTTP_400_BAD_REQUEST)

        formatted_user = accounts.v1.utils.generate_new_user_object(facebook_user, long_lived_fb_token)

        if 'app_version' in request.data:
            formatted_user['app_version'] = request.data['app_version']

        serializer = self.serializer_class(data=formatted_user)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)

        outdated = 'app_version' in request.data and request.data['app_version'] != settings.CURRENT_APP_VERSION

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response_data = {
            'token': token,
            'outdated': outdated,
            'facebook_access_token': user.facebook_access_token,
            'one_signal_id': user.one_signal_id,
            'user': {
                'facebook_uid': user.facebook_uid,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
        

class OneSignalView(AtomicMixin, GenericAPIView):
    serializer_class = OneSignalSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        """Save onSignal id."""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
