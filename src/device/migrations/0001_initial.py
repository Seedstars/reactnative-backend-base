# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceOrders',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('phone_number', models.CharField(max_length=16)),
                ('address', models.CharField(max_length=255, blank=True)),
                ('payment', models.CharField(default='P', max_length=1, choices=[('S', 'SIMPLE_PAY'), ('P', 'PAY_ON_DELIVERY')])),
                ('paid', models.CharField(default='N', max_length=1, choices=[('V', 'VERIFYING'), ('N', 'NOT_PAID'), ('P', 'PAID')])),
                ('date_request', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
