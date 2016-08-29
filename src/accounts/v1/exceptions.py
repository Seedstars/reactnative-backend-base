from rest_framework.exceptions import APIException


class FacebookInvalidTokenException(APIException):
    status_code = 400
    default_detail = 'The facebook token is invalid.'
