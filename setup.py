from setuptools import setup


setup(
    name='Django-Password-Protect',
    packages=['django_password_protect'],
    version='0.0.3',
    author='Andrew Plummer',
    author_email='plummer574@gmail.com',
    url='https://github.com/plumdog/django-password-protect',
    description='Middleware to add BasicAuth password protection to a site',
    test_suite='tests',
    install_requires=['Django', 'mock'])
