===================
Django Dynamic Form
===================

.. image:: https://img.shields.io/pypi/v/django-dynamic-forms.svg
   :target: https://pypi.python.org/pypi/django-dynamic-forms

.. image:: https://img.shields.io/pypi/l/django-dynamic-forms.svg
   :target: https://pypi.python.org/pypi/django-dynamic-forms

.. image:: https://img.shields.io/pypi/dm/django-dynamic-forms.svg
   :target: https://pypi.python.org/pypi/django-dynamic-forms


.. image:: https://img.shields.io/travis/MarkusH/django-dynamic-forms/master.svg
   :target: https://travis-ci.org/MarkusH/django-dynamic-forms

.. image:: https://img.shields.io/codecov/c/github/MarkusH/django-dynamic-forms/master.svg
   :target: https://codecov.io/github/MarkusH/django-dynamic-forms


**django-dynamic-forms** lets you create your forms through the Django admin.
You can add and remove form fields as you need them. That makes it perfect
for creating survey or application forms.

.. warning::

   **django-dynamic-forms** 0.5.x will only support Django >= 1.7! If you need
   support for Django < 1.7 use **django-dynamic-forms** 0.4.x!


INSTALLATION
============

Add ``'dynamic_forms.apps.DynamicFormsConfig'`` to the ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'dynamic_forms.apps.DynamicFormsConfig',
        ...
    )

Add ``'dynamic_forms.middlewares.FormModelMiddleware'`` to the
``MIDDLEWARE_CLASSES`` (probably at the end)::

    MIDDLEWARE_CLASSES = (
        ...
        'dynamic_forms.middlewares.FormModelMiddleware'
    )

Add ``'dynamic_forms.urls'`` to the URL patterns::

    urlpatterns = patterns('',
        ...
        url(r'^dynamic_forms/',
            include('dynamic_forms.urls', namespace='dynamic_forms')),
        ...
    )

.. important::

   Make sure that you get the namespace straight: ``dynamic_forms``!


You can set ``DYNAMIC_FORMS_EMAIL_RECIPIENTS`` in your settings to a list of
e-mail addresses. Forms being send via e-mail will then be send to those
addresses instead of those defined in ``settings.ADMINS``. Each recipient will
see *all* other recipients. See `send_mail
<https://docs.djangoproject.com/en/stable/topics/email/#django.core.mail.send_mail>`_
in the officiall documentation.


Example
=======

1. Change into the ``example/`` directory
2. Apply all migrations: ``python manage.py migrate``
3. Create a superuser (if not asked before): ``python manage.py createsuperuser``
4. Run ``python manage.py runserver``

The *admin* is available at http://127.0.0.1:8000/admin/.

You can find an example form at http://127.0.0.1:8000/example-form/.


Running the tests
=================

1. Make sure to install tox: ``$ pip install tox``
2. Run ``tox``
