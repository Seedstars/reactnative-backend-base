import factory
from django.test import TestCase

from device.models import DeviceOrders
from tests.v1.python.accounts.test_models import UserFactory


class DeviceOrdersFactory(factory.DjangoModelFactory):
    phone_number = '+41524204242'

    class Meta:
        model = DeviceOrders


class DeviceOrdersModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='test@example.com')
        self.device_order = DeviceOrdersFactory.create(user=self.user)

    def test_unicode(self):
        self.assertEqual(str(self.device_order), '{0}, John Doe'.format(self.device_order.id))
