from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lib.testutils import CustomTestCase
from tests.v1.python.accounts.test_serializers import LoginRegistrationSerializerTest

import responses


class AccountTests(CustomTestCase, APITestCase):
    @responses.activate
    def test_account_register_required_fields_successful(self):
        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                json=LoginRegistrationSerializerTest.FB_USER_INFO_REQUIRED,
                status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                json=LoginRegistrationSerializerTest.FB_LONG_LIVED_TOKEN, status=status.HTTP_200_OK, content_type='application/json')

        url = reverse('accounts_v1:login')
        response = self.client.post(url, LoginRegistrationSerializerTest.VALID_ACCESS_TOKEN, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_account_register_successful(self):
        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                json=LoginRegistrationSerializerTest.FB_USER_INFO,
                status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                json=LoginRegistrationSerializerTest.FB_LONG_LIVED_TOKEN, status=status.HTTP_200_OK, content_type='application/json')

        url = reverse('accounts_v1:login')
        response = self.client.post(url, LoginRegistrationSerializerTest.VALID_ACCESS_TOKEN, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_login_unsuccessful(self):
        self.assert_invalid_data_response(invalid_data_dicts=LoginRegistrationSerializerTest.INVALID_DATA_DICT,
                                          url=reverse('accounts_v1:login'))

    @responses.activate
    def test_facebook_exception(self):
        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json={"error": "error"},
                      status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        url = reverse('accounts_v1:login')
        response = self.client.post(url, LoginRegistrationSerializerTest.VALID_ACCESS_TOKEN, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_facebook_long_lived_token_exception(self):
        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=LoginRegistrationSerializerTest.FB_LONG_LIVED_TOKEN,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json={"error": "error"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        url = reverse('accounts_v1:login')
        response = self.client.post(url, LoginRegistrationSerializerTest.VALID_ACCESS_TOKEN, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)