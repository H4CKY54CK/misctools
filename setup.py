from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='misctools',
      version='1.4',
      description="'Miscellaneously Incredible Suite of Cool' TOOLS",
      long_description=readme(),
      author='Hackysack',
      author_email='tk13xr37@gmail.com',
      packages=['misctools'],
      install_requires=['progressbar2', 'pillow', 'praw'],
      python_requires='>=3.6',
      entry_points={'console_scripts':
          ['spriteit = misctools.spriteit:main',
          'zipit = misctools.zipit:main',
          'tarit = misctools.zipit:main',
          'wgetit = misctools.wgetit:main',
          'unzipit = misctools.unzipit:main',]
          })
