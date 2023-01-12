from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse

# https://help.wialon.com/help/wialon-local/2204/ru/how-tos/monitoring-system/how-to-configure-authorization-with-a-google-account
# https://console.cloud.google.com/apis/credentials
# https://it-stories.ru/blog/web-dev/avtorizacija-dlja-sajta-cherez-google/

def extern_auth_services(request):
    params = {
        'client_id': settings.EXTERN_AUTH['google']['client_id'],
        'redirect_uri': '{}{}'.format(settings.SITE_URL, reverse('extern_auth_google')),
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
        # 'state': '123',
    }
    google_auth_url = 'https://accounts.google.com/o/oauth2/auth?{}'.format(urlencode(params))
    return {'google_auth_url': google_auth_url}
