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
or stores it into the database (precisely the
:class:`~dynamic_forms.models.FormModelData` model).

Any action that should be available for usage must be registered in the
:class:`ActionRegistry`. This can be done with the following code::

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

.. versionadded:: 0.3

   When a dynamic form is submitted through
   :class:`~dynamic_forms.views.DynamicFormView` the return values of actions
   are kept for further usage. This allows the view to e.g. add a link to a
   permanent URL refering to some stored values.


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

      :param str key: The key to get an action
      :returns: Either the action previously registered or ``None`` if no
         action with the given key has been found.


   .. py:method:: get_as_choices()

      .. versionchanged:: 0.3
         Returns a generator instead of a list

      Returns a generator that yields all registered actions as 2-tuples in the
      form ``(key, label)``.


   .. py:method:: register(func, label)

      Registers the function ``func`` with the label ``label``. The function
      will internally be referred by it's full qualified name::

         '%s.%s' % (func.__module__, func.__name__)

      :param callable func: The function to register.
      :param str label: A string / unicode giving the action a human readable
        name


   .. py:method:: unregister(key)

      Looks up the given key in the internal dictionary and deletes the action
      if it exists.

      :param str key: The key an action is assigned to


.. py:data:: action_registry

   The singleton instance of the :class:`ActionRegistry`.


Action registry utilities
-------------------------

.. py:decorator:: formmodel_action(label)

   Registering various actions by hand can be time consuming. This function
   decorator eases this heavily: given a string as the first argument, this
   decorator registeres the decorated function withing the
   :data:`action_registry` with its fully dotted Python path.

   Usage:

   .. code-block:: python

      @formmodel_action('My super awesome action')
      def my_action(form_model, form):
         # do something with the data ...

   This is equivalent to:

   .. code-block:: python

      def my_action(form_model, form):
         # do something with the data ...

      action_registry.register(my_action, 'My super awesome action')


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

   This action takes the mapped data from the ``form`` and serializes it as
   JSON. This value is then stored in the
   :class:`~dynamic_forms.models.FormModelData`.

   .. seealso:: :func:`dynamic_form_store_database` for a detailed explaination
      of the arguments.

   .. versionadded:: 0.3

      To allow linking to a stored data set, the action now returns the
      inserted object.


