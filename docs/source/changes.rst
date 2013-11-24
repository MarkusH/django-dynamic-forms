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


v0.2
====

* Fixed some packaging issues (thanks Jannis Leidel)
* Add Django 1.7's db.migrations
* Moved to tox for development testing


v0.1
====

* Initital release
