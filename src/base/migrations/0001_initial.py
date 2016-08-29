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
            name='DiagnosticService',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('vehicle', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=16)),
                ('preferred_date', models.DateTimeField(null=True)),
                ('time_preference', models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening'), ('Afternoon', 'Afternoon')], default='Morning', max_length=10)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
