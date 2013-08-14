======
Models
======

.. py:module:: dynamic_forms.models


:class:`FormModel`
========================================

.. py:class:: FormModel()

   .. py:attribute:: name

      :class:`django.db.models.CharField`

      * max_length = 50
      * unique = ``True``

   .. py:attribute:: submit_url

      :class:`django.db.models.CharField`

      * max_length = 100
      * unique = ``True``

   .. py:attribute:: success_url

      :class:`django.db.models.CharField`

      * max_length = 100
      * unique = ``True``
      * blank = ``True``
      * default = ``''``

   .. py:attribute:: actions

      :class:`dynamic_forms.fields.TextMultiSelectField`

      * default = ``''``
      * choices = :meth:`dynamic_forms.actions.ActionRegistry.get_as_choices`

   .. py:attribute:: form_template

      :class:`django.db.models.CharField`

      * max_length = 100

   .. py:attribute:: success_template

      :class:`django.db.models.CharField`

      * max_length = 100


   .. py:attribute:: fields

      Related name by :class:`FormFieldModel`

   .. py:attribute:: data

      Related name by :class:`FormModelData`


   .. py:class:: Meta

      .. py:attribute:: ordering

         ``['name']``


   .. py:method:: __str__()
                  __unicode__()

   .. py:method:: get_fields_as_dict()

   .. py:method:: save([*args, **kwargs])


:class:`FormFieldModel`
=============================================

.. py:class:: FormFieldModel()

   .. py:attribute:: parent_form

      :class:`django.db.models.ForeignKey`

      * Foreign key to :class:`FormModel`
      * on_delete = :data:`django.db.models.CASCADE`

   .. py:attribute:: field_type

      :class:`django.db.models.CharField`

      * max_length = 255
      * choices = :meth:`dynamic_forms.formfields.DynamicFormFieldRegistry.get_as_choices`

   .. py:attribute:: label

      :class:`django.db.models.CharField`

      * max_length = 20

   .. py:attribute:: name

      :class:`django.db.models.CharField`

      * max_length = 50
      * blank = ``True``

   .. py:attribute:: _options

      :class:`django.db.models.TextField`

      * blank = ``True``
      * null = ``True``

   .. py:attribute:: position

      :class:`django.db.models.SmallIntegerField`

      * blank = ``True``
      * default = 0

   .. py:attribute:: options

      Property wrapping JSON serialization and deserialization around the :attr:`_options`.


   .. py:class:: Meta

      .. py:attribute:: ordering

         ``['parent_form', 'position']``

      .. py:attribute:: unique_together

         ``("parent_form", "name",)``


   .. py:method:: __str__()
                  __unicode__()

   .. py:method:: generate_form_field(form)

   .. py:method:: get_form_field_kwargs()

   .. py:method:: save([*args, **kwargs])


:class:`~dynamic_forms.models.FormModelData`
============================================

.. py:class:: FormModelData()

   .. py:attribute:: form

      :class:`django.db.models.ForeignKey`

      * Foreign key to :class:`FormModel`
      * on_delete = :data:`django.db.models.SET_NULL`
      * null = ``True``

   .. py:attribute:: value

      :class:`django.db.models.TextField`

      * blank = ``True``
      * default = ``''``

   .. py:attribute:: submitted

      :class:`django.db.models.DateTimeField`

      * auto_now_add = ``True``


   .. py:method:: __str__()
                  __unicode__()

   .. py:method:: pretty_value()
