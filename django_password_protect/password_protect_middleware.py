from django.http import HttpResponse
from django.conf import settings

import django

PASSWORD_PROTECT = getattr(settings, 'PASSWORD_PROTECT', True)
PASSWORD_PROTECT_USERNAME = getattr(settings, 'PASSWORD_PROTECT_USERNAME', None)
PASSWORD_PROTECT_PASSWORD = getattr(settings, 'PASSWORD_PROTECT_PASSWORD', None)
PASSWORD_PROTECT_REALM = getattr(settings, 'PASSWORD_PROTECT_REALM', 'Password Protected')


class PasswordProtectMiddleware(object):
    def process_request(self, request):
        if not PASSWORD_PROTECT:
            return

        if 'HTTP_AUTHORIZATION' in request.META:
            authentication = request.META['HTTP_AUTHORIZATION']
            auth_method, auth_credentials = authentication.split(' ', 1)
            if auth_method.lower() == 'basic':
                username, password = auth_credentials.strip().decode('base64').split(':', 1)
                if (username == settings.PASSWORD_PROTECT_USERNAME) and \
                   (password == settings.PASSWORD_PROTECT_PASSWORD):
                    return

        html = "<html><title>Auth required</title><body><h1>Authorization Required</h1></body></html>"
        if django.VERSION < 1.5:
            response_args = {'mimetype': 'text/html'}
        else:
            response_args = {'content_type': 'text/html'}

        response = HttpResponse(html, **response_args)
        response['WWW-Authenticate'] = 'Basic realm="{}"'.format(PASSWORD_PROTECT_REALM.replace('"', ''))
        response.status_code = 401
        return response
