========
Settings
========

.. py:module:: dynamic_forms.conf


:data:`DYNAMIC_FORMS_EMAIL_RECIPIENTS`
======================================

.. py:data:: DYNAMIC_FORMS_EMAIL_RECIPIENTS

   A list of email addresses. Used to define the receipients form data will be
   send to if the action :func:`~dynamic_forms.actions.dynamic_form_send_email`
   is activated.

   Defaults to all email addresses defined in the ``ADMINS`` setting.


:data:`DYNAMIC_FORMS_FORM_TEMPLATES`
====================================

.. py:data:: DYNAMIC_FORMS_FORM_TEMPLATES

   .. versionadded:: 0.3

   A tuple of 2-tuples passed to the :class:`~dynamic_forms.models.FormModel`'s
   `form_template` attribute. This setting provides easier and less error-prone
   definition of the form template.

   Defaults to:

   .. code-block:: python

       (
           ('dynamic_forms/form.html', _('Default form template')),
       )


:data:`DYNAMIC_FORMS_SUCCESS_TEMPLATES`
=======================================

.. py:data:: DYNAMIC_FORMS_SUCCESS_TEMPLATES

   .. versionadded:: 0.3

   A tuple of 2-tuples passed to the :class:`~dynamic_forms.models.FormModel`'s
   `success_template` attribute. This setting provides easier and less
   error-prone definition of the form template.

   .. code-block:: python

       (
           ('dynamic_forms/form_success.html', _('Default success template')),
       )
