=====
Views
=====

.. py:module:: dynamic_forms.views


.. autoclass:: DynamicFormView()
   :members: get_success_url, form_valid


.. autoclass:: DynamicTemplateView()
   :members: get_context_data


.. autoclass:: DynamicDataMixin()

   .. autoattribute:: slug_field

   ``'display_key'``

   .. autoattribute:: slug_url_kwarg

   ``'display_key'``

   .. autoattribute:: template_name_404

   ``'dynamic_forms/data_set_404.html'``


.. autoclass:: DynamicDataSetDetailView()

   .. autoattribute:: model

   The :class:`~dynamic_forms.models.FormDataModel`

   .. autoattribute:: template_name

   ``'dynamic_forms/data_set.html'``
