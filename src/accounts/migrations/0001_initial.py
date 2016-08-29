# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('first_name', models.CharField(default='Friend', verbose_name='First Name', max_length=50)),
                ('last_name', models.CharField(verbose_name='Last Name', blank=True, max_length=50)),
                ('email', models.EmailField(verbose_name='Email Address', blank=True, max_length=254)),
                ('facebook_uid', models.CharField(verbose_name='Facebook UID', max_length=50, unique=True)),
                ('one_signal_id', models.CharField(verbose_name='ONE Signal ID', blank=True, max_length=50)),
                ('gender', models.CharField(verbose_name='Gender', blank=True, max_length=25)),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser Status')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('facebook_access_token', models.CharField(verbose_name='Facebook Access Token', blank=True, max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
