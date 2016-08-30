import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeviceOrders(models.Model):
    """Model representing a Car Paper."""

    TYPE_SIMPLEPAY = 'S'
    TYPE_PAY_ON_DELIVERY = 'P'

    PAYMENT_TYPE = (
        (TYPE_SIMPLEPAY, 'SIMPLEPAY'),
        (TYPE_PAY_ON_DELIVERY, 'PAY ON DELIVERY')
    )

    PAYMENT_STATUS_VERIFYING = 'V'
    PAYMENT_STATUS_NOT_PAID = 'N'
    PAYMENT_STATUS_PAID = 'P'

    PAYMENT_STATUS = (
        (PAYMENT_STATUS_VERIFYING, 'VERIFYING'),
        (PAYMENT_STATUS_NOT_PAID, 'NOT PAID'),
        (PAYMENT_STATUS_PAID, 'PAID')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(_('Contact Phone'), max_length=16)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    payment = models.CharField(_('Contact Phone'),
                               max_length=1,
                               choices=PAYMENT_TYPE,
                               default=TYPE_PAY_ON_DELIVERY)
    paid = models.CharField(_('Payment Status'),
                            max_length=1,
                            choices=PAYMENT_STATUS,
                            default=PAYMENT_STATUS_NOT_PAID)
    date_request = models.DateTimeField(_('Order Date'), auto_now_add=True)

    def __str__(self):
        """String representation of the object."""
        return '{0}, {1} {2}'.format(self.id, self.user.first_name, self.user.last_name)
