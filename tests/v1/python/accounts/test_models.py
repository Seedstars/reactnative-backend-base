import uuid

import factory
from django.test import TestCase

from accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    first_name = 'John'
    last_name = 'Doe'
    is_active = True
    facebook_uid = str(uuid.uuid4())

    class Meta:
        model = User
        django_get_or_create = ('email',)


class AccountsModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='test@test.com')

    def test_unicode(self):
        self.assertEqual(str(self.user), 'test@test.com')

    def test_user(self):
        user = User.objects.create_user(email='email@test.com',
                                        first_name='user',
                                        last_name='test',
                                        facebook_uid=str(uuid.uuid4()),
                                        facebook_access_token='xxxxxxx')
        self.assertEqual(user.is_superuser, False)

    def test_superuser(self):
        user = User.objects.create_superuser(email='a@a.com',
                                             first_name='Friend',
                                             last_name='',
                                             password='test',
                                             facebook_uid=str(uuid.uuid4()),
                                             facebook_access_token='yyyyyyyyyy')
        self.assertEqual(user.is_superuser, True)
        self.assertTrue(user.check_password('test'))

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'John')
