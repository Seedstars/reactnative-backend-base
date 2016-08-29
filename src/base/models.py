"""Home app models."""

import uuid

from django.conf import settings
from django.db import models


class DiagnosticService(models.Model):
    """Model representing a Diagnostic Service."""

    TIME_PREFERENCE = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
        ('Afternoon', 'Afternoon'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    vehicle = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16)
    preferred_date = models.DateTimeField(null=True)
    time_preference = models.CharField(max_length=10, choices=TIME_PREFERENCE,
                                       default='Morning')

    def __str__(self):
        """String representation of the object."""
        return "{0}, {1} {2}".format(self.id, self.user.first_name, self.user.last_name)
