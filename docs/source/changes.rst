=======
Changes
=======

.. py:currentmodule:: dynamic_forms

v0.3
====

* Introduced the settings variables :data:`~conf.DYNAMIC_FORMS_FORM_TEMPLATES`
  and :data:`~conf.DYNAMIC_FORMS_SUCCESS_TEMPLATES` to make defining the
  templates for the form and success display easier and more usable for
  non-developers.
* Allow delayed registration of :doc:`actions <ref/actions>` and :doc:`dynamic
  form fields <ref/formfields>`.
* Allow dynamic fields to exclude their value from the ``mapped_data`` by
  overriding :classmethod:`~formfields.do_display_data`.
* Dropped support for Python 3.2. Nobody is really using it and it's a pain to
  integrate other libraries.
* Support for `django-simple-captcha <https://github.com/mbi/django-simple-captcha>`_
* Add Portuguese translation (thanks Gladson Simplicio)


v0.2
====

* Fixed some packaging issues (thanks Jannis Leidel)
* Add Django 1.7's db.migrations
* Moved to tox for development testing


v0.1
====

* Initital release
