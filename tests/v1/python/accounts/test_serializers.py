import responses
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.v1.serializers import LoginRegistrationSerializer
from lib.testutils import CustomTestCase
from tests.v1.python.accounts.test_models import UserFactory


class LoginRegistrationSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'email': 'test1@mailinator.com',
                  'first_name': 'test',
                  'last_name': 'user',
                  'gender': 'user',
                  'facebook_access_token': 'test'},
         'error': ('facebook_uid', ['This field is required.']),
         'label': 'Invalid request parameters.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
        {'data': {'email': 'test1@mailinator.com',
                  'facebook_uid': 'test',
                  'first_name': 'test',
                  'last_name': 'user',
                  'gender': 'user'},
         'error': ('facebook_access_token', ['This field is required.']),
         'label': 'Invalid request parameters.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
    ]
    VALID_ACCESS_TOKEN = {'access_token': 'xxxxxxxxxxxxxxxxxxxxx',
                          'app_version': '2.0.0'}

    FB_LONG_LIVED_TOKEN = {"access_token": "yyyyyyyyyyyyyyyyyy"}
    FB_USER_INFO = {"first_name": "Jon", "last_name": "Doe", "email": "jon@doe.com", "gender": "male",
                    "id": "1234567890"}
    FB_USER_INFO_REQUIRED = {"id": "1234567890"}

    def setUp(self):
        self.required_fields = ['facebook_uid', 'facebook_access_token']
        self.not_required_fields = ['first_name', 'last_name', 'gender', 'email']
        self.user = UserFactory.create(email='emailwilllogininserializer@mydomain.com')

    def test_fields(self):
        serializer = LoginRegistrationSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = LoginRegistrationSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    @responses.activate
    def test_validate_success(self):
        serializer = LoginRegistrationSerializer
        FORMATTED_FB_USER = [
            {"facebook_access_token": "xxxxxxxxxxx", "first_name": "Jon", "last_name": "Doe", "email": "jon@doe.com",
             "gender": "male", "facebook_uid": "1234567890"},
            {"facebook_access_token": "xxxxxxxxxxx", "first_name": "", "last_name": "", "email": "", "gender": "",
             "facebook_uid": "1234567890"},
            {"facebook_access_token": "xxxxxxxxxxx", "facebook_uid": "1234567890"}
        ]

        # Mock facebook 'get information' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/me',
                      json=self.FB_USER_INFO, status=status.HTTP_200_OK, content_type='application/json')

        # Mock facebook 'get long lived token' request
        responses.add(responses.GET, 'https://graph.facebook.com/v2.5/oauth/access_token',
                      json=self.FB_LONG_LIVED_TOKEN, status=status.HTTP_200_OK, content_type='application/json')
        self.assert_valid_data(serializer, FORMATTED_FB_USER)