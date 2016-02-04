import base64
from unittest import TestCase

import django
from django.conf import settings, global_settings
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from django_password_protect import PasswordProtectMiddleware

# Some ordering-sensitive imports
settings.configure(global_settings)
if not django.VERSION < (1, 7):
    django.setup()
from django.test import RequestFactory
from django.test.utils import override_settings


class MiddlewareTest(TestCase):

    maxdiff = 1000

    def process_request(self, **extra):
        request = RequestFactory().get('/fake-path/', **extra)

        middleware = PasswordProtectMiddleware()
        return middleware.process_request(request)

    def test_setting_disabled(self):
        with override_settings(PASSWORD_PROTECT=False):
            response = self.process_request()
        self.assertIsNone(response)

    def test_response_content(self):
        with override_settings(
                PASSWORD_PROTECT=True,
                PASSWORD_PROTECT_REALM='Test Realm'):
            response = self.process_request()
        self.assertEqual(response.status_code, 401)
        auth_content = response['WWW-Authenticate']
        self.assertEqual(auth_content, 'Basic realm="Test Realm"')
        self.assertEqual(
            smart_text(response.content),
            '<html><title>Auth required</title>'
            '<body><h1>Authorization Required</h1></body></html>')
        self.assertEqual(response['Content-Type'], 'text/html')

    def test_not_in_meta(self):
        with override_settings(PASSWORD_PROTECT=True):
            response = self.process_request()
        self.assertEqual(response.status_code, 401)

    def test_bad_auth_method(self):
        with override_settings(PASSWORD_PROTECT=True):
            response = self.process_request(
                HTTP_AUTHORIZATION=b'notbasic <credentials>')
        self.assertEqual(response.status_code, 401)

    def test_bad_username(self):
        auth_credentials = base64.encodestring(b'badusername:password')
        with override_settings(
                PASSWORD_PROTECT=True,
                PASSWORD_PROTECT_USERNAME='username',
                PASSWORD_PROTECT_PASSWORD='password'):
            response = self.process_request(
                HTTP_AUTHORIZATION=b'basic ' + auth_credentials)
        self.assertEqual(response.status_code, 401)

    def test_bad_password(self):
        auth_credentials = base64.encodestring(b'username:badpassword')
        with override_settings(
                PASSWORD_PROTECT=True,
                PASSWORD_PROTECT_USERNAME='username',
                PASSWORD_PROTECT_PASSWORD='password'):
            response = self.process_request(
                HTTP_AUTHORIZATION=b'basic ' + auth_credentials)
        self.assertEqual(response.status_code, 401)

    def test_correct_username_and_password(self):
        auth_credentials = base64.encodestring(b'username:password')
        with override_settings(
                PASSWORD_PROTECT=True,
                PASSWORD_PROTECT_USERNAME='username',
                PASSWORD_PROTECT_PASSWORD='password'):
            response = self.process_request(
                HTTP_AUTHORIZATION=b'basic ' + auth_credentials)
        self.assertIsNone(response)
