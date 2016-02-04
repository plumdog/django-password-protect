from django.http import HttpResponse
from django.conf import settings

from django.utils.encoding import smart_bytes
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

import base64


class PasswordProtectMiddleware(object):
    def __init__(self):
        self.PASSWORD_PROTECT = getattr(settings, 'PASSWORD_PROTECT', True)
        self.PASSWORD_PROTECT_USERNAME = getattr(settings, 'PASSWORD_PROTECT_USERNAME', None)
        self.PASSWORD_PROTECT_PASSWORD = getattr(settings, 'PASSWORD_PROTECT_PASSWORD', None)
        self.PASSWORD_PROTECT_REALM = getattr(settings, 'PASSWORD_PROTECT_REALM', 'Password Protected')

    def process_request(self, request):

        if not self.PASSWORD_PROTECT:
            return

        if 'HTTP_AUTHORIZATION' in request.META:
            authentication = smart_text(request.META['HTTP_AUTHORIZATION'], 'ascii')
            auth_method, auth_credentials = authentication.split(' ', 1)
            auth_credentials = auth_credentials.strip()

            if auth_method.lower() == 'basic':
                auth_credentials = base64.decodestring(smart_bytes(auth_credentials)).decode('ascii')
                username, password = auth_credentials.split(':', 1)
                if (username == self.PASSWORD_PROTECT_USERNAME) and \
                   (password == self.PASSWORD_PROTECT_PASSWORD):
                    return

        html = "<html><title>Auth required</title><body><h1>Authorization Required</h1></body></html>"
        response = HttpResponse(html, content_type='text/html')
        response['WWW-Authenticate'] = 'Basic realm="{}"'.format(self.PASSWORD_PROTECT_REALM.replace('"', ''))
        response.status_code = 401
        return response
