from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from device.models import DeviceOrders
from lib.v1.testutils import CustomTestCase, get_basic_auth_header
from tests.v1.python.accounts.test_models import UserFactory
from tests.v1.python.device.test_serializers import OrderDeviceSerializerTest


class OrderDeviceViewTests(CustomTestCase, APITestCase):
    def setUp(self):
        self.user = UserFactory(email='a@a.com')
        self.user.set_password('test')
        self.user.save()

    def test_invalid_data_response(self):
        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('a@a.com', 'test'))
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % response.data['token']))
        self.assert_invalid_data_response(invalid_data_dicts=OrderDeviceSerializerTest.INVALID_DATA_DICT,
                                          url=reverse('device_v1:order_device'))

    def test_order_device_success(self):
        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('a@a.com', 'test'))
        data = {'app_version': '1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % response.data['token']))

        url = reverse('device_v1:order_device')
        data = {'address': 'Street John 221',
                'phone_number': '+23412345678'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        device = DeviceOrders.objects.values('user', 'address', 'phone_number').latest('date_request')
        self.assertEqual(device['user'], self.user.pk)
        self.assertEqual(device['address'], data['address'])
        self.assertEqual(device['phone_number'], data['phone_number'])

        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('a@a.com', 'test'))
        data = {'app_version': '1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % response.data['token']))
        self.assertTrue(len(response.data['user']['device']) > 0)


class ValidateOrderDeviceViewTests(CustomTestCase, APITestCase):
    def setUp(self):
        self.user = UserFactory(email='a@a.com')
        self.user.set_password('test')
        self.user.save()

    def test_validate_order_device_success(self):
        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('a@a.com', 'test'))
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % response.data['token']))

        url = reverse('device_v1:validate_order_device_data')
        data = {'address': 'Street John 221',
                'phone_number': '+23412345678',
                'email': 'b@b.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
