import datetime

from django.core.urlresolvers import reverse
from django.utils.six import StringIO

from accounts.models import User
from lib.testutils import CustomTestCase, mock_send_email
from rest_framework import status
from rest_framework.test import APITestCase
import mock
import responses
from tests.v1.python.accounts.test_models import UserFactory
from tests.v1.python.accounts.test_serializers import LoginRegistrationSerializerTest
from tests.v1.python.home.test_models import ScheduleMaintenanceFactory, DiagnosticServiceFactory, PrePurchaseFactory


class HomeTests(APITestCase, CustomTestCase):
    @responses.activate
    @mock.patch('home.v1.utils.send_application_email', mock_send_email)
    def test_get_home_list(self):
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=LoginRegistrationSerializerTest.FB_USER_INFO,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request

        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=LoginRegistrationSerializerTest.FB_LONG_LIVED_TOKEN, status=status.HTTP_200_OK,
                      content_type='application/json')

        url = reverse('accounts_v1:login')
        response = self.client.post(url, LoginRegistrationSerializerTest.VALID_ACCESS_TOKEN, format='json')

        user = User.objects.first()

        self.scheduleMaintenance = ScheduleMaintenanceFactory.create(user=user)
        self.prePurchase = PrePurchaseFactory.create(user=user)
        self.diagnosticService = DiagnosticServiceFactory.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

        url = reverse('home_v1:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'vehicle': 'Opel',
                'location': 'Lagos',
                'phone_number': '+41524204242',
                'preferred_date': '2016-05-05T00:00:00+01:00',
                'time_preference': 'Morning'
                }

        url = reverse('home_v1:diagnostic-service')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'vehicle': 'Opel',
                'location': 'Lagos',
                'phone_number': '+41524204242',
                'preferred_date': '2016-05-05T00:00:00+01:00',
                'time_preference': 'Morning'
                }

        url = reverse('home_v1:pre-purchase-inspection')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'vehicle': 'Opel',
                'location': 'Lagos',
                'phone_number': '+41524204242',
                'preferred_date': '2016-05-05T00:00:00+01:00',
                'time_preference': 'Morning',
                'service_type': 'Basic',
                'oil_change':True
                }

        url = reverse('home_v1:schedule-maintenance')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'license_plate': '23-23-23',
                'phone_number': '+41524204242'
                }

        url = reverse('home_v1:car-papers')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'vehicle': 'opel',
                'phone_number': '+41524204242'
                }

        url = reverse('home_v1:diagnostic-scan')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'one_signal_id': 'asdasdasd',
                }
        url = reverse('home_v1:onesignal')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.first()
        self.assertEqual(user.one_signal_id, data['one_signal_id'])