# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, default=uuid.uuid4)),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name', default='Friend')),
                ('last_name', models.CharField(max_length=50, blank=True, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, blank=True, unique=True, verbose_name='Email Address')),
                ('facebook_uid', models.CharField(max_length=50, unique=True, verbose_name='Facebook UID')),
                ('one_signal_id', models.CharField(max_length=50, blank=True, verbose_name='ONE Signal ID')),
                ('gender', models.CharField(max_length=25, blank=True, verbose_name='Gender')),
                ('branch_data', models.TextField(blank=True, verbose_name='Referrer')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True, verbose_name='Phone Number')),
                ('app_version', models.CharField(max_length=5, blank=True, verbose_name='App Version')),
                ('is_staff', models.BooleanField(verbose_name='Staff Status', default=False)),
                ('is_superuser', models.BooleanField(verbose_name='Superuser Status', default=False)),
                ('is_active', models.BooleanField(verbose_name='Active', default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('facebook_access_token', models.CharField(max_length=250, blank=True, verbose_name='Facebook Access Token')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
