#!/usr/bin/env python3
# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from __future__ import annotations
# -- Imports ----------------------------------------------------------------
import os
import sys
import pathlib as pl
import datetime

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use pl.Path.resolve to make it absolute, like shown here.
#
sys.path.insert(0, str(pl.Path('.tasks/sphinxcode').resolve()))

# -- Project information -----------------------------------------------------

project        = 'Bibliography'
author         = 'John Grey'
copyright      = '{}, {}'.format(datetime.datetime.now().strftime("%Y"), author)
primary_domain = "bibtex"
html_baseurl   = "https://bibliography.github.io"
extensions     = [
    'sphinx.ext.napoleon',
    'sphinx.ext.extlinks',
    'sphinx_rtd_theme',
    'myst_parser',
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # "sphinx_sitemap",
]

source_suffix = {
    ".rst" : "restructuredtext",
    ".md"  : "markdown",

}
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "**/.git",
    "**/.github",
    "**/__tests/*",
    ".venv/*",
    ".site/*",
    "bookmarks/*",
    "completions/*",
    "in_progress/*",
    "main/*",
    "plus/*",
    # "tags/*",
    "timelines/*",
    '**flycheck_*.py',
    "readme.md",
]

include_patterns = ["**"]
# suppress_warnings = ["autoapi", "docutils"]

# -- Path setup --------------------------------------------------------------

# (Relative to this file):
templates_path   = ['static_/templates']
html_static_path = ['static_']
html_extra_path  = []

# --------------------------------------------------------------------------
# Relative to static dir, or fully qualified urls
html_css_files = ["css/custom.css"]
html_js_files  = ["js/base.js"]

toc_object_entries            = True
master_doc                    = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

maximum_signature_line_length = 50
toc_object_entries            = True
show_warning_types            = True

# -- Options for HTML output -------------------------------------------------
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme          = "sphinx_rtd_theme"
html_theme_options  = {}
html_sidebars       = {}
html_domain_indices = True
html_use_index      = True
html_split_index    = True

html_theme_options.update({
    'logo_only'                   : False,
    # 'display_version'             : True,
    'prev_next_buttons_location'  : 'bottom',
    'style_external_links'        : False,
    'vcs_pageview_mode'           : '',
    'style_nav_header_background' : 'grey',
    # TOC options:
    'collapse_navigation'         : True,
    'sticky_navigation'           : True,
    'navigation_depth'            : 4,
    'includehidden'               : True,
    'titles_only'                 : False

})

# -- Sphinx and Jina configuration -------------------------------------------
import sphinx_bib_domain

def setup(app):
    app.events.connect("builder-inited", add_jinja_ext, 0)
    sphinx_bib_domain.setup(app)

def add_jinja_ext(app):
    app.builder.templates.environment.add_extension('jinja2.ext.debug')
