import json
from django_rest_logger import log
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from device.v1.serializers import OrderDeviceSerializer
from accounts.v1.serializers import UserEmailUpdateSerializer
from lib.v1.utils import AtomicMixin
from device.v1.utils import message_order_device, send_application_email


class OrderDeviceView(AtomicMixin, GenericAPIView):
    serializer_class = OrderDeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Pre Purchase Inspection solicitation."""
        log.info('OrderDeviceView::post::data: {}'.format(json.dumps(request.data)))

        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_device = serializer.create(serializer.validated_data)

        msg = message_order_device(order_device)
        send_application_email(msg, 'New MileFriend Order Device')

        return Response(status=status.HTTP_200_OK)


class ValidateOrderDeviceView(AtomicMixin, GenericAPIView):
    serializer_class = OrderDeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Pre Purchase Inspection solicitation."""
        log.info('ValidateOrderDeviceView::post::data: {}'.format(json.dumps(request.data)))

        request_data = request.data.copy()
        request_data['user'] = request.user.id

        if 'email' in request_data:
            serializer = UserEmailUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user, serializer.validated_data)

        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)
