# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
from sphinx.ext import autodoc
import logging



project = 'MiniCPM-V & o Cookbook'
copyright = '2025, OpenBMB'
author = 'OpenBMB'
release = 'V4.0'

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "myst_parser",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    # "sphinx_copybutton",
]

myst_enable_extensions = ["colon_fence", "attrs_block", "attrs_inline", "fieldlist"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = project
html_theme = 'furo'
html_static_path = ['_static']



# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Exclude the prompt "$" when copying code
copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = project
html_theme = "furo"
# html_logo = 'assets/logo/minicpm.png'
# html_theme_options = {
#     'path_to_docs': 'docs/source',
#     'repository_url': 'https://github.com/OpenBMB/MiniCPM',
#     # 'use_repository_button': True,
# }
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# multi-language docs
language = "en"
locale_dirs = ["../locales/"]  # path is example but recommended.
gettext_compact = False  # optional.
gettext_uuid = True  # optional.

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
# FIXME: figure out why this file is not copied
html_js_files = [
    "design-tabs.js",
    "analytics.js",
]

# Mock out external dependencies here.
autodoc_mock_imports = ["torch", "transformers"]

for mock_target in autodoc_mock_imports:
    if mock_target in sys.modules:
        logger.info(
            f"Potentially problematic mock target ({mock_target}) found; "
            "autodoc_mock_imports cannot mock modules that have already "
            "been loaded into sys.modules when the sphinx build starts."
        )


class MockedClassDocumenter(autodoc.ClassDocumenter):
    """Remove note about base class when a class is derived from object."""

    def add_line(self, line: str, source: str, *lineno: int) -> None:
        if line == "   Bases: :py:class:`object`":
            return
        super().add_line(line, source, *lineno)


autodoc.ClassDocumenter = MockedClassDocumenter

navigation_with_keys = False

# Sitemap
html_baseurl = 'https://minicpm-o.readthedocs.io/'
sitemap_url_scheme = "{lang}/{version}/{link}"
sitemap_locales = ["en", "zh_CN"]
sitemap_filename = "sitemap.xml"

# Open Graph
ogp_site_url = "https://minicpm-o.readthedocs.io/"
ogp_description_length = 200
ogp_image = "https://raw.githubusercontent.com/OpenBMB/MiniCPM/refs/heads/main/assets/minicpm_logo.png"
ogp_image_width = 1200
ogp_image_height = 630
ogp_type = "website"
ogp_site_name = "MiniCPM-V & o Cookbook"
ogp_use_first_image = True

ogp_locale_alternate = [
    ("en_US", "https://minicpm-o.readthedocs.io/en/latest/"),
    ("zh_CN", "https://minicpm-o.readthedocs.io/zh_CN/latest/"),
]

# HTML head meta tags
html_context = {
    'en': {
        'meta_description': 'MiniCPM-V & o Cookbook - Your step-by-step guide to running MiniCPM models anywhere',
        'meta_keywords': 'MiniCPM, Large Language Model, AI, Machine Learning, Documentation',
        'meta_author': 'OpenBMB',
        'meta_robots': 'index, follow',
        'canonical_url': 'https://minicpm-o.readthedocs.io/en/latest/',
    },
    'zh_CN': {
        'meta_description': 'MiniCPM-V & o Cookbook - 完整的MiniCPM模型使用指南',
        'meta_keywords': 'MiniCPM, 大语言模型, AI, 机器学习, 文档',
        'meta_author': 'OpenBMB',
        'meta_robots': 'index, follow',
        'canonical_url': 'https://minicpm-o.readthedocs.io/zh_CN/latest/',
    }
}

def get_language_meta():
    current_lang = language
    return html_context.get(current_lang, html_context['en'])

html_context.update(get_language_meta())

html_use_index = True
html_split_index = False
html_compressed = True

html_extra_path = ['_static/robots.txt']