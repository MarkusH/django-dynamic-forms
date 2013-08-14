=====
Forms
=====

.. py:module:: dynamic_forms.forms


Form Fields
===========

.. py:class:: MultiSelectFormField([separate_values_by='\\n', **options])

   Provides multiple choice field storage for string objects without limiting
   the total length of the string.

   :param str separate_values_by: The string used to split the input value into
      its choices. Defaults to ``'\n'``.

   .. seealso::

      The respective database field as part of **django-dynamic-forms**
      :class:`dynamic_forms.fields.TextMultiSelectField`. :ref:`The core form
      field arguments <django:core-field-arguments>` and the specifics for the
      :class:`django.forms.MultipleChoiceField`.

   .. note::

      The implementation is based on http://djangosnippets.org/snippets/2753/
      but has been modified to the needs of this project.

Forms
=====

.. py:class:: FormModelForm(model [, *args, **kwargs])

   .. py:method:: get_mapped_data([exclude_missing=False])

      Returns an dictionary sorted by the position of the respective field in
      its form.

      :param boolean exclude_missing: If ``True``, non-filled fields (those
         whose value evaluates to ``False``) are not present in the returned
         dictionary. Default: ``False``
