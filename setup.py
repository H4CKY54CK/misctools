from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='misctools',
      version='1.6',
      description="'Miscellaneously Incredible Suite of Cool' TOOLS",
      long_description=readme(),
      author='Hackysack',
      author_email='tk13xr37@gmail.com',
      packages=['misctools'],
      install_requires=['tqdm', 'pillow'],
      python_requires='>=3.6',
      entry_points={'console_scripts':
          ['spriteit = misctools.spriteit:main',
          'archit = misctools.archit:main',
          'wgetit = misctools.wgetit:main',
          'unzipit = misctools.unzipit:main',
          'ipy = misctools.utilities:main',
          'untarit = misctools.unzipit:main',]
          })
