import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def _create_user(self, email, facebook_uid, facebook_access_token, first_name, last_name, password, is_staff,
                     is_superuser, **extra_fields):
        """
        Create and save an User with the given email, facebook_uid, facebook_access_token, name and phone number.

        :param email: string
        :param facebook_uid: string
        :param facebook_access_token: string
        :param first_name: string
        :param last_name: string
        :param is_staff: boolean
        :param is_superuser: boolean
        :param extra_fields:
        :return: User
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          facebook_uid=facebook_uid,
                          facebook_access_token=facebook_access_token,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now, **extra_fields)
        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, facebook_uid, facebook_access_token, **extra_fields):
        """
        Create and save an User with the given email, facebook_uid and name.

        :param email: string
        :param first_name: string
        :param last_name: string
        :param facebook_uid: string
        :param facebook_access_token: string
        :param extra_fields:
        :return: User
        """

        return self._create_user(email, facebook_uid, facebook_access_token, first_name, last_name, password=None,
                                 is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, facebook_uid, facebook_access_token,
                         **extra_fields):
        """
        Create a super user.

        :param email: string
        :param password: string
        :param first_name: string
        :param last_name: string
        :param facebook_uid: string
        :param facebook_access_token: string
        :param extra_fields:
        :return: User
        """
        return self._create_user(email, facebook_uid, facebook_access_token, first_name, last_name, password,
                                 is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser):
    """Model that represents an user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('First Name'), max_length=50, default='Friend')
    last_name = models.CharField(_('Last Name'), max_length=50, blank=True)
    email = models.EmailField(_('Email Address'), blank=True, unique=True)
    facebook_uid = models.CharField(_('Facebook UID'), max_length=50, unique=True)
    one_signal_id = models.CharField(_('ONE Signal ID'), max_length=50, blank=True)
    gender = models.CharField(_('Gender'), max_length=25, blank=True)
    branch_data = models.TextField(_('Referrer'), blank=True)
    phone_number = PhoneNumberField(_('Phone Number'), blank=True)

    app_version = models.CharField(_('App Version'), max_length=5, blank=True)

    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_superuser = models.BooleanField(_('Superuser Status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)

    facebook_access_token = models.CharField(_('Facebook Access Token'), max_length=250, blank=True)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        """
        Unicode representation for an user model.

        :return: string
        """
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.

        :return: string
        """
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        """
        Return the first_name.

        :return: string
        """
        return self.first_name
