django-password-protect
=======================
Middleware to BasicAuth password protection to a site.

Currently just supports a single username/password combination, and is
either every url, or none.

This is basically just a slight tweak to the snippet here:
https://djangosnippets.org/snippets/2468/ by joshsharp. Just adds some
settings and bundles it up into a package.

TODO:
+ add option for a url regex to specify which urls require auth.
+ be able to set a list of usernames/password, possibly add the option
  for this to look at a model, though this may be out of scope. Not
  sure.
+ tests

Getting Started
---------------

```pip install django-password-protect```

Then add `'django_password_protect.PasswordProtectMiddleware'` to `MIDDLEWARE_CLASSES` in your `settings.py`.

Then set the following settings, also in `settings.py`:

`PASSWORD_PROTECT`: bool, defaults to True. Should the site be
password protected? So if set to False, this middleware does nothing
at all.

`PASSWORD_PROTECT_USERNAME`: str, defaults to None (meaning no login
is possible). The username to allow login.

`PASSWORD_PROTECT_PASSWORD`: str, defaults to None (meaning no login
is possible). The password to allow login.

`PASSWORD_PROTECT_REALM`: str, defaults to `"Password Protected"`. This is displayed when the basic-auth password prompt appears, saying something like:

Authentication Required: The site says: "[[PASSWORD_PROTECT_REALM]]"
