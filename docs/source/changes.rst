=======
Changes
=======

.. py:currentmodule:: dynamic_forms

v0.5 (under development)
========================

* Form action take a required third argument ``request``.
* Support for Django 1.9
* Removed ``six`` dependency
* Added missing contrib packages (thanks Seán Hayes) (#23)


v0.4.1 (SECURITY RELEASE)
=========================

* Fixed a CSRF vulnerability in the ``POST`` handling of forms. Thanks
 `Marten Kenbeek <https://github.com/knbk>`_ for the report and patch. (#26)


v0.4
====

* Added support for Django 1.8 and experimental support for Django 1.9. (#19)
* Removed ``django-appconf`` dependency.
* Added per form email receivers (thanks to Nar Chhantyal). (#13)
* Increased form fields' label ``max_length`` to 255 (thanks to Nar Chhantyal).
  (#18)


v0.3.4
======

* Fixed a issue with missing migrations on Python 2. (#11)


v0.3.3
======

* Updated Portuguese translation (thanks Gladson Simplicio). (#8)


v0.3.2
======

* Introduced the settings variables :data:`~conf.DYNAMIC_FORMS_FORM_TEMPLATES`
  and :data:`~conf.DYNAMIC_FORMS_SUCCESS_TEMPLATES` to make defining the
  templates for the form and success display easier and more usable for
  non-developers. (#1)
* Allowed delayed registration of :doc:`actions <ref/actions>` and
  :doc:`dynamic form fields <ref/formfields>`.
* Allowed dynamic fields to exclude their value from the ``mapped_data`` by
  overriding :meth:`~formfields.do_display_data`.
* Added support for `django-simple-captcha
  <https://github.com/mbi/django-simple-captcha>`_. (#2)
* Added Portuguese translation (thanks Gladson Simplicio). (#4)
* Replaced :data:`formfields.dynamic_form_field_registry` with
  :data:`formfields.formfield_registry` and deprecated the former.
* Fixed sorting of actions and field types by their label. (#5)
* Allowed users to get a link to see the data they submitted before at a later
  time. (#6)


v0.2
====

* Fixed some packaging issues. (thanks Jannis Leidel)
* Added Django 1.7's db.migrations.
* Moved to tox for development testing.


v0.1
====

* Initial release
