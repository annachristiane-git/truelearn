# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import inspect
import warnings
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(".."))


# We need to clean up the generated folder and gallery, otherwise the
# old files will be left and Sphinx will not rebuild them.
path_modules = Path("./modules/generated/")
path_gallery = Path("./docs/examples/")

if path_modules.exists():
    shutil.rmtree(str(path_modules))
if path_gallery.exists():
    shutil.rmtree(str(path_gallery))


project = "TrueLearn"
# pylint: disable=redefined-builtin
copyright = "2023, TrueLearn"
author = "TrueLearn Team"

import truelearn

version = truelearn.__version__
release = truelearn.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx_copybutton",
    # for some mysterious reason, if we put sphinx_gallery
    # below autosummary (which means if it is loaded after autosummary),
    # trueskill in truelearn.learning will not be properly
    # imported (``dir(trueskill)`` does not include trueskill
    # methods and classes and ``trueskill.__all__`` is an empty list)
    #
    # Note: An alternative solution is to add a higher priority of
    # ``generate_gallery_rst`` method in ``sphinx_gallery.gen_gallery``
    # which controls the gallery generation. It is registered via
    # app.connect('builder-inited', generate_gallery_rst).
    "sphinx_gallery.gen_gallery",
    "sphinx.ext.autosummary",
]
templates_path = ["templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for autodoc extension -------------------------------------------
autodoc_mock_imports = ["trueskill", "sklearn", "mpmath"]

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "mpmath": ("https://mpmath.org/doc/current/", None),
    "trueskill": ("https://trueskill.org/", None),
}

# -- Options for linkcode extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html
# Code below from:
# https://github.com/Lasagne/Lasagne/blob/master/docs/conf.py#L114


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to the sourcecode."""

    def find_source():
        # Find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286

        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)

        # only links to truelearn modules
        fullname = ".".join([obj.__module__, obj.__name__])
        if not fullname.startswith("truelearn"):
            raise RuntimeError("Not a truelearn module")

        fn = inspect.getsourcefile(obj)
        if fn is not None:
            fn = os.path.relpath(fn, start=os.path.dirname(truelearn.__file__))
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != "py" or not info["module"]:
        return None

    try:
        source_info = find_source()
        filename = f"truelearn/{source_info[0]}#L{source_info[1]}-L{source_info[2]}"
    except Exception:
        # no source code found
        # return None, so [source] is not linked incorrectly
        return None

    tag = "main" if "dev" in version else version
    return f"https://github.com/TrueLearnAI/truelearn/blob/{tag}/{filename}"


# -- Gallery configuration ---------------------------------------------------
from plotly.io._sg_scraper import plotly_sg_scraper
from sphinx_gallery.sorting import ExampleTitleSortKey

image_scrapers = (
    "matplotlib",
    plotly_sg_scraper,
)

sphinx_gallery_conf = {
    "reference_url": {
        # The module you locally document uses None
        "truelearn": None,
    },
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "examples",  # path to where to save gallery generated output,
    "download_all_examples": False,  # disable download file buttons
    "within_subsection_order": ExampleTitleSortKey,  # sort examples by title
    "remove_config_comments": True,
    "show_memory": False,
    "show_signature": False,
    "plot_gallery": "True",
    "image_scrapers": image_scrapers,
}

# filter WordPlotter warnings because we already have
# an admonition in the WordPlotter example
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=(
        "WordPlotter may be removed in a future release "
        "because wordcloud library does not have "
        r"cross-platform support for Python 3.11\+, "
        r"and it is not actively maintained\."
    ),
)

# -- Options for napoleon extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_include_special_with_doc = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_logo = "images/TrueLearn_logo.png"
html_css_files = ["custom.css"]
html_static_path = ["_static"]

# -- Options for Furo theme --------------------------------------------------
html_theme_options = {
    "light_css_variables": {
        "color-api-background": "#f8f9fb",
    },
    "dark_css_variables": {
        "color-api-background": "#1e1e1e",
    },
}
