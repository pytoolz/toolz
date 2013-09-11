from os.path import exists
from setuptools import setup

setup(name='toolz',
      version='0.1',
      description='More tools',
      url='http://github.com/mrocklin/toolz',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['toolz'],
      install_requires=[
          "itertoolz >= 0.5",
          "functoolz >= 0.4",
      ],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
