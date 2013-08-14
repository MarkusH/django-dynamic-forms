=======
Actions
=======

.. py:module:: dynamic_forms.actions

Actions define what happens once a user submits a
:class:`~dynamic_forms.forms.FormModelForm`. **django-dynamic-forms** provides
two basic actions :func:`~dynamic_form_send_email` and
:func:`~dynamic_form_store_database` that, as their names indicate, either
send the submitted data via e-mail to the receipients defined in the
:data:`~dynamic_forms.conf.DYNAMIC_FORMS_EMAIL_RECIPIENTS` settings variable
or stores it into the database (precisely the :class:`~FormModelData` model).

Any action that should be available for usage must be registered in the :class:`ActionRegistry`. This can be done with the following code::

   >>> def my_function(form_model, form):
   ...     # do something
   ...     pass
   ...
   >>> from dynamic_forms.actions import action_registry
   >>> action_registry.register(my_function, 'My Label')

This allows one to register an action during runtime. But many actions are
already available during compile or start-up time and can be registered then by
using a handy decorator :func:`formmodel_action`. Given the above situation,
this would look like::

   >>> from dynamic_forms.actions import formmodel_action
   >>> @formmodel_action('My Label')
   ... def my_function(form_model, form):
   ...     # do something
   ...     pass
   ...


Providing and accessing actions
===============================

:class:`ActionRegistry`
-----------------------

.. py:class:: ActionRegistry()

   The ActionRegistry keeps track of all available actions available to the
   software. It is available to the outside through the
   :data:`action_registry` singleton

   .. warning::

      You should not import the :class:`ActionRegistry` directly! Always use
      the singleton instance :data:`action_registry`!

      >>> from dynamic_forms.actions import action_registry


   .. py:method:: get(key)

   .. py:method:: get_as_choices()

   .. py:method:: register(func, label)

      Registers the function ``func`` with the label ``label``. The function
      will internally be referred by it's full qualified name::

         '%s.%s' % (func.__module__, func.__name__)

      :param callable func: The function to register.
      :param str label: A string / unicode giving the action a human readable
        name


   .. py:method:: unregister(key)


.. py:data:: action_registry


Action registry utilities
-------------------------

.. py:decorator:: formmodel_action(label)


Default Actions
===============

.. py:function:: dynamic_form_send_email(form_model, form)

   Sends the data submitted through the form ``form`` via e-mail to all
   recipients listed in
   :data:`~dynamic_forms.conf.DYNAMIC_FORMS_EMAIL_RECIPIENTS`.

   :param dynamic_forms.models.FormModel form_model: The instance of the model
      defining the form.
   :param dynamic_forms.forms.FormModelForm form: The instance of the submitted
      form. One can get the data either using ``form.cleaned_data`` or, if the
      labels defined in the ``form_model`` for each field are needed, in the
      appropriate order by calling
      :meth:`~dynamic_forms.forms.FormModelForm.get_mapped_data`.


.. py:function:: dynamic_form_store_database(form_model, form)
