# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
openpd_dir = os.path.join(cur_dir, '../..')
sys.path.insert(0, openpd_dir)
import os
import sys

# -- Project information -----------------------------------------------------

project = 'OpenPD'
copyright = '2021, Southeast University and Zhenyu Wei'
author = 'Zhenyu Wei'

# The full version, including alpha/beta/rc tags
release = '0.1'
version = '0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

autodoc_member_order = 'bysource'

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = project
# html_theme = 'alabaster'
# html_theme = "sphinx_rtd_theme"
# html_theme = 'karma_sphinx_theme'
# html_theme = 'asteroid_sphinx_theme'
# html_theme = "sphinx_material"
# html_theme = "furo"
# extensions.append("faculty_sphinx_theme")
# html_theme = "faculty-sphinx-theme"
html_theme = "sphinx_material"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_theme_options = {
    'repo_url': 'https://github.com/zhenyuwei99/openpd',
    'repo_name': 'OpenPD',
    'repo_type': 'github',
    'logo_icon': '&#xe869',
    'nav_title': ' ',
    'globaltoc_depth': -1,
    'color_primary': 'indigo'
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}