=====
Usage
=====

Using Custom Templates
======================

**django-dynamic-forms** comes with a basic template that just displays the form
or a success page. You can customize these templates to your needs.


The Form Template
-----------------

The following code shows the default template rendering a dynamic form.

.. literalinclude:: ../../dynamic_forms/templates/dynamic_forms/form.html
   :language: html+django

The :class:`~dynamic_forms.views.DynamicFormView` exposes three variables to the
template context related to the form:

``form``
   An instance of the form that will be shown on this page. As the form is a
   normal Django form, all rules from the
   `Django documentation <https://docs.djangoproject.com/en/dev/topics/forms/#displaying-a-form-using-a-template>`_
   apply.

``model``
   An instance of the form model providing the form and assigned to this URL.

``name``
   The form's name as defined in :attr:`dynamic_forms.models.FormModel.name`.

``success_url``
   The URL the form will be submitted to as defined in
   :attr:`dynamic_forms.models.FormModel.submit_url`. This is *not* the
   :attr:`~dynamic_forms.models.FormModel.success_url`!


The Success Template
--------------------

The following code shows the success template after a successful form submit.

.. literalinclude:: ../../dynamic_forms/templates/dynamic_forms/form_success.html
   :language: html+django

The :class:`~dynamic_forms.views.DynamicTemplateView` exposes three variables to
the template context related to the form:

``model``
   An instance of the form model assigned to this URL.
