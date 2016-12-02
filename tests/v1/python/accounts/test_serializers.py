import responses
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.v1.serializers import LoginRegistrationSerializer, OneSignalSerializer, UserRegistrationSerializer, \
    UserEmailUpdateSerializer, UserAppVersionUpdateSerializer
from lib.v1.testutils import CustomTestCase
from tests.v1.python.accounts.test_models import UserFactory


class LoginRegistrationSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'email': 'test1@example.com',
                  'facebook_uid': 'test',
                  'first_name': 'test',
                  'last_name': 'user',
                  'gender': 'user',
                  'facebook_access_token': 'test'},
         'error': ('email', ['Email is invalid.']),
         'label': 'Invalid email.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
        {'data': {'email': 'test1@a.com',
                  'facebook_uid': 'test',
                  'first_name': 'test',
                  'last_name': 'user',
                  'gender': 'user',
                  'facebook_access_token': 'test',
                  'app_version': '1.0.0'},
         'error': ('app_version', ['App version not valid.']),
         'label': 'Invalid app version format.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         }
    ]
    VALID_DATA_DICT = [
        {'facebook_access_token': 'xxxxxxxxxxx',
         'first_name': 'Jon',
         'last_name': 'Doe',
         'email': 'jon@doe.com',
         'gender': 'male',
         'facebook_uid': '1234567890'},
        {'facebook_access_token': 'xxxxxxxxxxx',
         'first_name': '',
         'last_name': '',
         'email': '',
         'gender': '',
         'facebook_uid': '1234567890'},
        {'facebook_access_token': 'xxxxxxxxxxx',
         'first_name': 'Jon',
         'last_name': 'Doe',
         'email': 'jon@doe.com',
         'gender': 'male',
         'facebook_uid': '1234567890',
         'app_version': '1.0'},
        {'facebook_access_token': 'xxxxxxxxxxx',
         'facebook_uid': '1234567890'}
    ]

    def setUp(self):
        self.required_fields = ['facebook_uid', 'facebook_access_token']
        self.not_required_fields = ['first_name', 'last_name', 'gender', 'email', 'branch_data', 'app_version', 'id']

        self.user = UserFactory.create(email='emailwilllogininserializer@mydomain.com')
        self.fb_long_lived_token = {'access_token': 'yyyyyyyyyyyyyyyyyy'}
        self.fb_user_info = {'first_name': 'Jon',
                             'last_name': 'Doe',
                             'email': 'jon@doe.com',
                             'gender': 'male',
                             'id': '1234567890'}

    def test_fields(self):
        serializer = LoginRegistrationSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = LoginRegistrationSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    @responses.activate
    def test_valid_data(self):
        serializer = LoginRegistrationSerializer

        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=self.fb_user_info, status=status.HTTP_200_OK, content_type='application/json')
        # Mock facebook 'get long lived token' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=self.fb_long_lived_token, status=status.HTTP_200_OK, content_type='application/json')

        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class OneSignalSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = []
    VALID_DATA_DICT = [
        {'one_signal_id': '1234567890'},
        {'one_signal_id': ''}
    ]

    def setUp(self):
        self.required_fields = ['one_signal_id']
        self.not_required_fields = []

    def test_fields(self):
        serializer = OneSignalSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = OneSignalSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_valid_data(self):
        serializer = OneSignalSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class UserEmailUpdateSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'email': 'test1@mailinator.com'},
         'error': ('email', ['Email is invalid.']),
         'label': 'Invalid email.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
    ]
    VALID_DATA_DICT = [
        {'email': 'a@a.com'}
    ]

    def setUp(self):
        self.required_fields = ['email']
        self.not_required_fields = []

    def test_fields(self):
        serializer = UserEmailUpdateSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = UserEmailUpdateSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_valid_data(self):
        serializer = UserEmailUpdateSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class UserAppVersionUpdateSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'app_version': '1.0.0.'},
         'error': ('app_version', ['App version not valid.']),
         'label': 'Invalid app version format.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
    ]
    VALID_DATA_DICT = [
        {'app_version': '1.0'}
    ]

    def setUp(self):
        self.required_fields = ['app_version']
        self.not_required_fields = []

    def test_fields(self):
        serializer = UserAppVersionUpdateSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = UserAppVersionUpdateSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_valid_data(self):
        serializer = UserAppVersionUpdateSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class UserRegistrationSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'email': 'test1@mailinator.com',
                  'name': 'John Doe',
                  'password': 'test',
                  'confirm_password': 'test'},
         'error': ('email', ['Please use a different email address provider.']),
         'label': 'Invalid email.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
        {'data': {'email': 'test1@gmail',
                  'name': 'John Doe',
                  'password': 'test',
                  'confirm_password': 'test'},
         'error': ('email', ['Enter a valid email address.']),
         'label': 'Bad email format.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
        {'data': {'email': 'a@a.com',
                  'name': 'John Doe',
                  'password': 'test',
                  'confirm_password': 'test',
                  'app_version': '2.0.0'},
         'error': ('app_version', ['App version not valid.']),
         'label': 'App version not valid.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
        {'data': {'email': 'b@b.com',
                  'name': 'John Doe',
                  'password': 'test',
                  'confirm_password': 'test',
                  'app_version': '2.0'},
         'error': ('email', ['Email already in use, please use a different email address.']),
         'label': 'User with email already exists.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
        {'data': {'email': 'a@a.com',
                  'name': 'John Doe',
                  'password': 'test',
                  'confirm_password': 'test2',
                  'app_version': '2.0'},
         'error': ('non_field_errors', ['Passwords don\'t match.']),
         'label': 'Password and confirm password don\'t match.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         }
    ]
    VALID_DATA_DICT = [
        {'email': 'emailsuccess@a.com',
         'name': 'John Doe',
         'password': 'test',
         'confirm_password': 'test'},
        {'email': 'emailsuccess@a.com',
         'name': 'John Doe',
         'app_version': '1.0',
         'password': 'test',
         'confirm_password': 'test'},
    ]

    def setUp(self):
        self.required_fields = ['email', 'name', 'password', 'confirm_password']
        self.not_required_fields = ['app_version', 'branch_data']
        self.user = UserFactory(email='b@b.com')

    def test_fields(self):
        serializer = UserRegistrationSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = UserRegistrationSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_valid_data(self):
        serializer = UserRegistrationSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)
