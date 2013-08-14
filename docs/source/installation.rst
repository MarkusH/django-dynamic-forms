============
Installation
============

Install **django-dynamic-forms** into your virtual environment or you
site-packages using pip:

.. code-block:: console

   $ pip install django-dynamic-forms

If you already use the wheel package format you can use the wheel build:

.. code-block:: console

   $ pip install --use-wheel django-dynamic-forms

To make **django-dynamic-forms** available in your Django project, you first
have to add it to the ``INSTALLED_APPS`` in your ``settings.py``. If you are unsure where to put it,
just append it:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dynamic_forms',
        ...
    )

To make Django aware of the dynamic forms while processing the requests /
responses you need to add the ``FormModelMiddleware`` to the list of
``MIDDLEWARE_CLASSES``. The best place is probably at the end of the list. If
your forms are not shown please refer to the :doc:`known problems <problems>`
section of the documentation:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'dynamic_forms.middlewares.FormModelMiddleware'
    )

Finally you have to update your database. If you use `South
<http://south.aeracode.org/>`_ you need to run:

.. code-block:: console

   $ python manage.py syncdb
   $ python manage.py migrate

otherwise, if you don't use South, you have to run:

.. code-block:: console

   $ python manage.py syncdb
