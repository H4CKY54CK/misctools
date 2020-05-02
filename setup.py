import re
from setuptools import find_packages, setup
from codecs import open
from os import path
HERE = path.abspath(path.dirname(__file__))
PACKAGE_NAME = 'misctools'
with open(path.join(HERE, PACKAGE_NAME, "__init__.py"), encoding="utf-8") as fp:
    VERSION = re.search('__version__ = "([^"]+)"', fp.read()).group(1)

with open('README.md') as f:
    README = f.read()

setup(name=PACKAGE_NAME,
      version=VERSION,
      description="'Miscellaneously Incredible Suite of Cool' TOOLS",
      long_description=README,
      author='Hackysack',
      author_email='tk13xr37@gmail.com',
      packages=find_packages(exclude=[]),
      install_requires=['pillow'],
      python_requires='>=3.6',
      entry_points={'console_scripts':
          ['spriteit = misctools.spriteit:main',
          'archit = misctools.archit:main',
          'wgetit = misctools.wgetit:main',
          'unarchit = misctools.archit:umain',
          'gifit = misctools.gifit:main',
          'sliceit = misctools.sliceit:main',
          'wcit = misctools.utilities:wcit.start',]
          })

