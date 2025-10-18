#!/usr/bin/env python3
"""
Configuration file for the Sphinx documentation builder.
https://www.sphinx-doc.org/en/master/usage/configuration.html

CWD is the dir of this file.

- https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
- https://pygments.org/docs/lexers
- https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
- https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
- https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
- https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
- https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
- https://www.sphinx-doc.org/en/master/usage/extensions/imgconverter.html
- https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
- https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
- https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
- https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html
"""
# ruff: noqa: TC003, A001, DTZ005, ERA001, PLR2044, ARG001, ANN001, ANN201, TC002
from __future__ import annotations
##-- imports
import os
import sys
import pathlib as pl
import datetime
from collections.abc import Sequence, Callable
import tomllib
from typing import Literal
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.locale import __
from sphinx.util.docutils import SphinxDirective

##-- end imports

##-- types
exclude_patterns                      : list[str]
extensions                            : list[str]
highlight_options                     : dict
html_domain_indices                   : bool|Sequence[str]
html_additional_pages                 : dict
html_search_options                   : dict
html_js_files                         : list
html_sidebars                         : dict
html_static_path                      : list
html_theme_path                       : list
html_extra_path                       : list
html_style                            : list[str] | str
include_patterns                      : list[str]
needs_extensions                      : dict[str, str]
nitpick_ignore                        : set[tuple[str, str]]
nitpick_ignore_regex                  : set[tuple[str, str]]
source_suffix                         : dict[str, str]
templates_path                        : list[str]
napoleon_type_aliases                 : dict
python_maximum_signature_line_length  : int | None
autoapi_prepare_jinja_env : Callable[[jinja2.Environment], None] | None
type InterTuple      = tuple[str, tuple[str, str | None] | None]
intersphinx_mapping      : dict[str, InterTuple]
intersphinx_cache_limit  : int
intersphinx_timeout      : int | float | None
extlinks : dict[str, tuple[str, str]]
##-- end types

_target = pl.Path.cwd() / "pyproject.toml"
assert(_target.exists())
pyproject  = tomllib.loads(_target.read_text())

##-- project settings
project                        = pyproject['project']['name']
author                         = "John Grey"
copyright                      = "{}, {}".format(datetime.datetime.now().strftime("%Y"), author)
language                       = "en"
release                        = pyproject['project']['version']

root_doc                       = "index"
primary_domain                 = "py"
default_role                   = None

root_doc                       = "index"
suppress_warnings               = [
    "docutils",
]
maximum_signature_line_length  = 50
toc_object_entries             = True
add_function_parentheses       = True
show_warning_types             = True
nitpick_ignore                 = set()
nitpick_ignore_regex           = set()

needs_extensions               = {
    # ExtName : Version
}
extensions                     = []

##-- end project settings

##-- locations
# Relative to this file/config directory:
templates_path    = [
    "./templates_",
]
html_theme_path   = []
html_static_path  = ["./static_"]
html_extra_path   = []  # for things like robots.txt

# Relative to html_static_path , or fully qualified urls:
html_css_files       = [
    "css/custom.css",
]
html_js_files        = [
    "js/custom.js",
]

# load path modification:
# local_mod = str(pl.Path.cwd().parent.parent)
# sys.path.insert(0, local_mod)

##-- end locations

##-- file types
source_suffix = {
    ".rst"  : "restructuredtext",
    # ".txt"  : "restructuredtext",
    ".md"   : "markdown",
    ".bib"  : "bibtex"
}

##-- end file types

##-- exclusion
# List of patterns, relative to *source directory*, that match files and
# directories to incldue/ignore when looking for source files.
# These also affect html_static_path and html_extra_path.
include_patterns = [
    # "**",
    "index.rst",
    "report.rst",
    "pages_/*",
    # ".temp/export/rst/*",
    "*main/*",
    # "*plus/*",
    # "*plus/conferences_primary/aisb_/bibtex/*",
    # "*plus/individuals/*",
    ]
exclude_patterns = []

# ignore doc directories
# and polyglot util directories
exclude_patterns += [
    # "main/*",
    "plus/*",
    "bookmarks/*",
    "completions/*",
    "in_progress/*",
    "readme.md",
    "timelines/*",
    "**/.git",
    "**/.github",
    "**/__tests/*",
    "**/flycheck_*.py",
    ".temp/mypy*",
    ".temp/site"
    ".temp/tox",
    ".venv/*",
    "static_/",
    # "tags/*",
    '**flycheck_*.py',
]

# ignore tests and util files
exclude_patterns += [
    "conf.py",
    "README.md",
]

##-- end exclusion

##-- bibtex domain
extensions.append("sphinx_bib_domain")
bib_domain_split_index = True

##-- end bibtex domain

##-- html
html_use_index                = False
html_split_index              = True
html_permalinks               = True
html_copy_source              = True
html_show_sourcelink          = True
html_show_search_summary      = False
html_codeblock_linenos_style  = "inline"  # or "table"
# --
html_theme_options     = {}
html_sidebars          = {} # Maps doc names -> templates
html_additional_pages  = {} # Maps doc names -> templates
html_context           = {}
html_search_options    = {}
html_domain_indices  = True
# html_domain_indices    = []
# html_style           = []
# html_logo            = ""
html_favicon      = "static_/favicon.ico"
# Generate additional domain specific indices
# html_domain_indices.append("py-modindex")
html_additional_pages.update({})
html_context.update({
    "collapse_index_py": True,
    "collapse_index_jg": True,
})

##-- end html

##-- readthedocs theme
extensions.append("sphinx_rtd_theme")
html_theme                = "sphinx_rtd_theme"
html_theme_options.update({
    "logo_only"                   : False,
    "prev_next_buttons_location"  : "bottom",
    "style_external_links"        : False,
    "vcs_pageview_mode"           : "",
    "style_nav_header_background" : "grey",
    # TOC options:
    "collapse_navigation"         : True,
    "sticky_navigation"           : True,
    "navigation_depth"            : 4,
    "includehidden"               : True,
    "titles_only"                 : False,
})

##-- end readthedocs theme

##-- markdown
extensions.append("myst_parser")

##-- end markdown

##-- rst preprocessing
# rst_prolog = ""
# rst_epilog = ""

##-- end rst preprocessing

##-- python domain
add_module_names                                = True
python_display_short_literal_types              = False
python_trailing_comma_in_multi_line_signatures  = True
python_user_unqualified_type_names              = False
trim_doctest_flags                              = True
# Remove prefixes for indexiing
modindex_common_prefix                = [
    "The", "the"
]
python_maximum_signature_line_length  = None

##-- end python domain

##-- pygments syntax highlighting

highlight_options              = {}
pygments_style                 = "sphinx"

##-- end pygments syntax highlighting

##-- graphviz
# https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html
extensions.append("sphinx.ext.graphviz")
# Command name to invoke dot:
graphviz_dot            =  "dot"
graphviz_dot_args       = ()
graphviz_output_format  = "svg"  # or "dot"

##-- end graphviz

##-- image conversion
# imagemagick conversion: https://www.sphinx-doc.org/en/master/usage/extensions/imgconverter.html
extensions.append("sphinx.ext.imgconverter")
image_converter       = "convert"
image_converter_args  = ()

##-- end image conversion

##-- jinja customisation
try:
    import jinja2
except ImportError:
    jinja2 = None
else:

    def filter_contains(val:list|str, *needles:str) -> bool:
        match val:
            case str():
                return any(x in val for x in needles)
            case list():
                joined = " ".join(val)
                return any(x in joined for x in needles)
            case _:
                return False

    def autoapi_prepare_jinja_env(jinja_env: jinja2.Environment) -> None:
        """Add a custom jinja test """
        jinja_env.add_extension("jinja2.ext.debug")
        jinja_env.tests['contains'] = filter_contains

    def add_jinja_ext(app):
        app.builder.templates.environment.add_extension("jinja2.ext.debug")

##-- end jinja customisation

#-- Sphinx and Jinja configuration ------------

def setup(app):
    # if jinja2 is not None:
    #     app.events.connect("builder-inited", add_jinja_ext, 1)
    pass

# -- Debug output --------------------------------------------------
def pg_out(val):
    print(f"[polyglot]: {val}")

pg_out("Exclusion Patterns:")
for x in sorted(exclude_patterns):
    pg_out(f"- '{x}'")
else:
    pg_out("----")

pg_out("Active Extensions:")
for x in sorted(extensions):
    pg_out(f"- {x}")
else:
    pg_out("----")
    pg_out(f"CWD: {pl.Path.cwd()}")
    pg_out("initialisation complete")
