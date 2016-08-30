from rest_framework import status
from rest_framework.test import APITestCase

from device.v1.serializers import OrderDeviceSerializer, GetOrderDeviceListSerializer
from lib.v1.testutils import CustomTestCase
from tests.v1.python.accounts.test_models import UserFactory


class OrderDeviceSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {
            'data': {
                'user': 1,
                'address': 'Street John 221',
                'phone_number': '+35190123450232'
            },
            'error': ('phone_number', ['Phone number is not valid.']),
            'label': 'Invalid phone number format.',
            'method': 'POST',
            'status': status.HTTP_400_BAD_REQUEST
        }
    ]
    VALID_DATA_DICT = [
        {
            'user': 1,
            'address': 'Street John 221',
            'phone_number': '+23412345678'
        },
    ]

    def setUp(self):
        self.required_fields = ['user', 'address', 'phone_number']
        self.not_required_fields = ['id', 'payment']
        self.user = UserFactory(id=1, email='a@a.com')

    def test_fields(self):
        serializer = OrderDeviceSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = OrderDeviceSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_valid_data(self):
        serializer = OrderDeviceSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class GetOrderDeviceListSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = []
    VALID_DATA_DICT = []

    def setUp(self):
        self.required_fields = ['user', 'phone_number']
        self.not_required_fields = ['id', 'address', 'payment', 'paid']

    def test_fields(self):
        serializer = GetOrderDeviceListSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = GetOrderDeviceListSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_valid_data(self):
        serializer = GetOrderDeviceListSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)
