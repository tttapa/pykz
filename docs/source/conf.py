# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
import shutil
from sphinx_gallery.scrapers import figure_rst
project = 'pykz'
copyright = '2025, Mathijs Schuurmans'
author = 'Mathijs Schuurmans'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'myst_parser',
    'sphinx_gallery.gen_gallery',
    "sphinx_codeautolink",
]

templates_path = ['_templates']
exclude_patterns = []


# Define custom PDF scraper
sys.path.insert(0, os.path.abspath('..'))


def pdf_scraper(block, block_vars, gallery_conf):
    """Scrape PDFs and move them to the right directory."""
    image_path_iterator = block_vars['image_path_iterator']
    examples_dir = os.path.dirname(block_vars['src_file'])
    pdf_files = []

    # Look for PDFs in the example directory
    for pdf in os.listdir(examples_dir):
        if pdf.endswith('.pdf'):
            # Get next image path (with .png extension)
            image_path = next(image_path_iterator)
            pdf_path = os.path.join(examples_dir, pdf)
            # Copy PDF to build directory
            shutil.copy(pdf_path, image_path.replace('.png', '.pdf'))
            pdf_files.append(image_path)
            # Remove the original PDF
            os.remove(pdf_path)

    # Create RST to display PDF links
    if pdf_files:
        pdf_rst = ""
        for pdf_file in pdf_files:
            png_name = os.path.basename(pdf_file)
            pdf_name = png_name.replace('.png', '.pdf')
            pdf_rst += f"""
.. only:: html

    `Download {pdf_name} <{pdf_name}>`_

"""
        return pdf_rst
    return ''


sphinx_gallery_conf = {
    'examples_dirs': '../../examples',   # Path from conf.py to examples folder
    'recommender': {"enable": True, "n_examples": 5, "min_df": 3, "max_df": 0.9},
    'gallery_dirs': 'gallery',     # This will be created relative to doc build
    'filename_pattern': '/',
    'image_scrapers': (pdf_scraper),  # Add PDF scraper
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
