import sys, os
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer

sys.path.append(os.path.abspath('_exts'))

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['configurationblock']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

highlight_language = 'php'

project = u'Silex'
copyright = u'2010 Fabien Potencier'

version = '0'
release = '0.0.0'

lexers['php'] = PhpLexer(startinline=True)

html_theme_path = ['./_themes/']
html_static_path = ['_static']

html_theme = 'symfony-japan-docs'