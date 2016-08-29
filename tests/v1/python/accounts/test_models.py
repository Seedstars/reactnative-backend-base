import factory
from django.test import TestCase

from accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    first_name = 'John'
    last_name = 'Doe'
    is_active = True

    class Meta:
        model = User
        django_get_or_create = ('email',)


class AccountsModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='test@test.com')

    def test_unicode(self):
        self.assertEqual(str(self.user), 'test@test.com')

    def test_user(self):
        user = User.objects.create_user(email='email@test.com', first_name='user', last_name='test', facebook_uid='xxxxx', facebook_access_token='xxxxxxx')
        self.assertEqual(user.is_superuser, False)
        user = User.objects.create_user(email='', first_name='Friend', last_name='', facebook_uid='yyyyy', facebook_access_token='yyyyyy')
        self.assertEqual(user.is_superuser, False)

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'John')