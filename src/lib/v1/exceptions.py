from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class FacebookInvalidTokenException(APIException):
    status_code = 400
    default_detail = _('The facebook token is invalid.')
