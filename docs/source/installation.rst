============
Installation
============

.. warning::

   **django-dynamic-forms** 0.5.x will only support Django >= 1.7! If you need
   support for Django < 1.7 use **django-dynamic-forms** 0.4.x!

Install **django-dynamic-forms** into your virtual environment or you
site-packages using pip:

.. code-block:: console

   $ pip install django-dynamic-forms

If you already use the wheel package format you can use the wheel build:

.. code-block:: console

   $ pip install --use-wheel django-dynamic-forms

To make **django-dynamic-forms** available in your Django project, you first
have to add it to the ``INSTALLED_APPS`` in your ``settings.py``. If you are
unsure where to put it, just append it:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dynamic_forms.apps.DynamicFormsConfig',
        ...
    )

To make Django aware of the dynamic forms while processing the requests /
responses you need to add the ``FormModelMiddleware`` to the list of
``MIDDLEWARE_CLASSES`` (or ``MIDDLEWARE`` for Django 1.10+). The best place is
probably at the end of the list. If your forms are not shown please refer to
the :doc:`known problems <problems>` section of the documentation:

.. code-block:: python

    MIDDLEWARE_CLASSES = (  # Django <= 1.9
        ...
        'dynamic_forms.middlewares.FormModelMiddleware'
    )

    MIDDLEWARE = (  # Django >= 1.10
        ...
        'dynamic_forms.middlewares.FormModelMiddleware'
    )

Last but not least you need to add the ``'dynamic_forms.urls'`` urlpatterns to
your project's URL patterns::

    urlpatterns = patterns('',
        ...
        url(r'^dynamic_forms/',
            include('dynamic_forms.urls', namespace='dynamic_forms')),
        ...
    )

.. important::

   Make sure that you get the namespace straight: ``dynamic_forms``!


Finally you have to update your database. Run:

.. code-block:: console

   $ python manage.py migrate dynamic_forms
