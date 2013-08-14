========
Problems
========

My form is not shown
====================

If you are sure you followed the :doc:`installation` instructions, there are several reasons:

1. You might have misspelled the URL path. Please check again.
2. There is another view that maps to the URL you defined in your model.
   1. If you have Django's flatpages framework installed, check please check that there is not page mapping to this URL.
3. An error occurs while constructing the form or rendering the template. Set ``DEBUG = True`` in your ``settings.py`` and have a look at the exception that is raised.
