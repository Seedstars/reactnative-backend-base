import json

import responses
import shortuuid
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from lib.v1.testutils import CustomTestCase, get_basic_auth_header
from tests.v1.python.accounts.test_models import UserFactory
from tests.v1.python.accounts.test_serializers import LoginRegistrationSerializerTest, OneSignalSerializerTest, \
    UserRegistrationSerializerTest


class AccountFacebookTests(CustomTestCase, APITestCase):
    def test_invalid_data(self):
        self.assert_invalid_data_response(invalid_data_dicts=LoginRegistrationSerializerTest.INVALID_DATA_DICT,
                                          url=reverse('accounts_v1:login_facebook'))

    @responses.activate
    def test_account_register_required_fields_successful(self):
        # Mock facebook 'get information' request
        response_data = {'first_name': 'Jon',
                         'last_name': 'Doe',
                         'email': 'jon@doe.com',
                         'gender': 'male',
                         'id': '1234567890'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=response_data,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        response_data = {'access_token': 'yyyyyyyyyyyyyyyyyy'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=response_data, status=status.HTTP_200_OK,
                      content_type='application/json')

        url = reverse('accounts_v1:login_facebook')
        data = {'access_token': 'xxxxxxxxxxxxxxxxxxxxx', 'app_version': '2.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_account_register_successful_with_branch_data(self):
        # Mock facebook 'get information' request
        response_data = {'first_name': 'Jon',
                         'last_name': 'Doe',
                         'email': 'jon@doe.com',
                         'gender': 'male',
                         'id': '1234567890'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=response_data,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        response_data = {'access_token': 'yyyyyyyyyyyyyyyyyy'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=response_data, status=status.HTTP_200_OK,
                      content_type='application/json')

        url = reverse('accounts_v1:login_facebook')
        data = {'access_token': 'xxxxxxxxxxxxxxxxxxxxx', 'app_version': '2.0', 'branch_data': {'key1': '23456'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.values('email', 'branch_data').latest('date_joined')
        self.assertEqual(user['email'], 'jon@doe.com')
        self.assertEqual(json.loads(user['branch_data']), data['branch_data'])

    @responses.activate
    def test_account_register_successful_without_facebook_email(self):
        # Mock facebook 'get information' request
        response_data = {'first_name': 'Jon',
                         'last_name': 'Doe',
                         'gender': 'male',
                         'id': '1234567890'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=response_data,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        response_data = {'access_token': 'yyyyyyyyyyyyyyyyyy'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=response_data, status=status.HTTP_200_OK,
                      content_type='application/json')

        url = reverse('accounts_v1:login_facebook')
        data = {'access_token': 'xxxxxxxxxxxxxxxxxxxxx', 'app_version': '2.0', 'branch_data': {'key1': '23456'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.values('email', 'branch_data').latest('date_joined')
        self.assertTrue(user['email'].endswith('temporary.com'))
        self.assertEqual(json.loads(user['branch_data']), data['branch_data'])

    @responses.activate
    def test_facebook_exception(self):
        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json={'error': 'error'},
                      status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        url = reverse('accounts_v1:login_facebook')
        data = {'access_token': 'xxxxxxxxxxxxxxxxxxxxx', 'app_version': '2.0'}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['access_token'], [_('The facebook token is invalid.')])

    @responses.activate
    def test_facebook_long_lived_token_exception(self):
        # Mock facebook 'get information' request
        response_data = {'access_token': 'yyyyyyyyyyyyyyyyyy'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=response_data,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json={'error': 'error'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        url = reverse('accounts_v1:login_facebook')
        data = {'access_token': 'yyyyyyyyyyyyyyyyyy'}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['access_token'], [_('The facebook token is invalid.')])


class OneSignalTests(CustomTestCase, APITestCase):
    def test_invalid_data(self):
        self.assert_invalid_data_response(invalid_data_dicts=OneSignalSerializerTest.INVALID_DATA_DICT,
                                          url=reverse('accounts_v1:onesignal'))

    @responses.activate
    def test_one_signal_with_data(self):
        # Mock facebook 'get information' request
        response_data = {'first_name': 'Jon',
                         'last_name': 'Doe',
                         'email': 'jon@doe.com',
                         'gender': 'male',
                         'id': '1234567890'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=response_data,
                      status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        response_data = {'access_token': 'yyyyyyyyyyyyyyyyyyyyyyy'}
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=response_data, status=status.HTTP_200_OK,
                      content_type='application/json')

        url = reverse('accounts_v1:login_facebook')
        data = {'access_token': 'xxxxxxxxxxxxxxxxxxxxx', 'app_version': '2.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        url = reverse('accounts_v1:onesignal')
        data = {'one_signal_id': '123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.values('one_signal_id').latest('date_joined')
        self.assertEqual(user['one_signal_id'], data['one_signal_id'])


class AccountTests(CustomTestCase, APITestCase):
    def setUp(self):
        self.user = UserFactory.create(email='emailwilllogininserializer@mydomain.com')

    def test_invalid_data(self):
        self.user = UserFactory(email='b@b.com', facebook_uid=shortuuid.uuid())
        self.assert_invalid_data_response(invalid_data_dicts=UserRegistrationSerializerTest.INVALID_DATA_DICT,
                                          url=reverse('accounts_v1:register'))

    def test_register_success(self):
        url = reverse('accounts_v1:register')
        data = {'email': 'emailsuccess@myspecialemail.com',
                'name': 'John Doe',
                'password': 'test',
                'confirm_password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.values('email', 'first_name', 'last_name').latest('date_joined')
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['first_name'], 'John')
        self.assertEqual(user['last_name'], 'Doe')

        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('emailsuccess@myspecialemail.com', 'test'))
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % response.data['token']))

        url = reverse('accounts_v1:onesignal')
        data = {'one_signal_id': '123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.values('one_signal_id').latest('date_joined')
        self.assertEqual(user['one_signal_id'], data['one_signal_id'])

        url = reverse('accounts_v1:logout')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('accounts_v1:onesignal')
        data = {'one_signal_id': '123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_duplicated_email(self):
        url = reverse('accounts_v1:register')
        data = {'email': 'emailsuccess@myspecialemail.com',
                'name': 'John Doe',
                'password': 'test',
                'confirm_password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.values('email', 'first_name', 'last_name').latest('date_joined')
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['first_name'], 'John')
        self.assertEqual(user['last_name'], 'Doe')

        url = reverse('accounts_v1:register')
        data = {'email': 'emailsuccess@myspecialemail.com',
                'name': 'John Doe',
                'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  #
        self.assertEqual(response.data['email'], ['Email already in use, please use a different email address.'])

    def test_login_app_version_invalid(self):
        url = reverse('accounts_v1:register')
        data = {'email': 'emailsuccess@myspecialemail.com',
                'name': 'John Doe',
                'password': 'test',
                'confirm_password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.values('email', 'first_name', 'last_name').latest('date_joined')
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['first_name'], 'John')
        self.assertEqual(user['last_name'], 'Doe')

        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('emailsuccess@myspecialemail.com', 'test'))
        data = {'app_version': '1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('accounts_v1:login')
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header('emailsuccess@myspecialemail.com', 'test'))
        data = {'app_version': '1.0.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['app_version'], ['App version not valid.'])
