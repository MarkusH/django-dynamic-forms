#!/usr/bin/env python
import sys
from os.path import abspath, dirname, join

sys.path.insert(0, abspath(join(dirname(__file__), '..', '..')))

from dynamic_forms import get_version

# -- General configuration -----------------------------------------------------

project = 'django-dynamic-forms'
copyright = '2013, Markus Holtermann'
version = get_version(full=False)
release = get_version()

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
exclude_patterns = []

master_doc = 'index'
source_suffix = '.rst'

pygments_style = 'sphinx'
templates_path = ['_templates']

intersphinx_mapping = {
    'django': ('https://docs.djangoproject.com/en/dev/',
               'https://docs.djangoproject.com/en/dev/_objects/'),
    'python2': ('http://docs.python.org/2/', None),
    'python3': ('http://docs.python.org/3/', None),
}

# -- Options for HTML output ---------------------------------------------------
html_theme = 'nature'
html_static_path = ['_static']
htmlhelp_basename = 'django-dynamic-formsdoc'
modindex_common_prefix = ['dynamic_forms.']
