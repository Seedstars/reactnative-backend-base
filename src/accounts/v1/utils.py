import urllib
import facebook
from django.conf import settings

from lib.v1.exceptions import FacebookInvalidTokenException


def generate_long_lived_fb_token(access_token, graph_api):
    """Generate a long lived facebook token."""
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'fb_exchange_token': access_token
    }
    connection_name = 'access_token?{}'.format(urllib.parse.urlencode(params))

    try:
        long_lived_fb_token = graph_api.get_connections(id='oauth', connection_name=connection_name)
    except facebook.GraphAPIError:
        raise FacebookInvalidTokenException

    return long_lived_fb_token['access_token']


def get_facebook_user(graph_api):
    """Get the user information from Facebook."""
    params = ['id', 'first_name', 'last_name', 'gender', 'email']
    graph_object_id = 'me?fields={}'.format(','.join(params))

    try:
        facebook_user = graph_api.get_object(id=graph_object_id)
    except facebook.GraphAPIError:
        raise FacebookInvalidTokenException

    return facebook_user
