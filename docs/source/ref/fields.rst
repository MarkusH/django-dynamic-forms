======
Fields
======

.. py:module:: dynamic_forms.fields

.. py:class:: TextMultiSelectField([separate_values_by='\\n', **options])

   Provides multiple choice field storage for strings without limiting
   the total length of the string or giving any restrictions of which characters
   are not allowed because they are used to split the input value into its
   different choices.

   :param str separate_values_by: The string used to split the input value into
      its choices. Defaults to ``'\n'``.

   .. seealso::

      The respective form field as part of **django-dynamic-forms**
      :class:`dynamic_forms.forms.MultiSelectFormField`. :ref:`The common field
      options <django:common-model-field-options>` and the specifics for the
      :class:`django.db.models.TextField`.

   .. note::

      The implementation is based on http://djangosnippets.org/snippets/2753/ but
      has been modified to the needs of this project. Thus, there is no conversion
      of the selected items to ``int`` or similar.
