from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse


def extern_auth_services(request):
    params = {
        'client_id': settings.EXTERN_AUTH['google']['client_id'],
        'redirect_uri': '{}{}'.format(settings.SITE_URL, reverse('extern_auth_google')),
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    }
    google_auth_url = 'https://accounts.google.com/o/oauth2/auth?{}'.format(urlencode(params))
    return {'google_auth_url': google_auth_url}
