===========
Middlewares
===========

.. py:module:: dynamic_forms.middlewares

.. py:class:: FormModelMiddleware()

   This middleware intercepts all HTTP 404 responses and checks if there is a
   form mapped to this URL. This way an explicit URL mapping from the projects
   ROOT_URLCONF cannot accidentally be overridden by wrong setting for
   :attr:`~dynamic_forms.models.FormModel.submit_url` or
   :attr:`~dynamic_forms.models.FormModel.success_url` on
   :class:`dynamic_forms.models.FormModel`.

   This technique is comparable to the one used by Django's :class:`~django.contrib.flatpages.FlatpageFallbackMiddleware`.

   .. py:method:: process_response(request, response)

      The algorithm that decides if and which form to display works like this:

      1. If the ``status_code`` for ``response`` is **not** 404 (``NOT FOUND``)
         this the :class:`FormModelMiddleware` will return the response as-is
         and will not modify it. Thus, server error (5xx) will also not be
         affected by the middleware.
      2. If there is a :class:`~dynamic_forms.models.FormModel` whose
         :attr:`~dynamic_forms.models.FormModel.submit_url` matches the
         request's ``path_info``, this model is used to construct and render the
         view.
      3. If there is a :class:`~dynamic_forms.models.FormModel` whose
         :attr:`~dynamic_forms.models.FormModel.success_url` matches the
         request's ``path_info``, this model is used to display the success
         page.

         .. note::

            Since the ``success_url`` of a ``FormModel`` is not necessarily be
            unique, the first model that matches the request path will be used.
      4. If any errors occur while processing a form the original request is
         returned (if ``DEBUG = True`` the respective exception is raised).
