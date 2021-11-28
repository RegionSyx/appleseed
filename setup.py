#!/usr/bin/env python

from distutils.core import setup

setup(name='appleseed',
      version='0.1',
      description='Let This code for you!',
      author='Eric Hurst',
      author_email='eric.hurst97@gmail.com',
      packages=['appleseed'],
      entry_points={
          'console_scripts': ['appleseed=appleseed.cli:cli'],
      },
      install_requires=[
          'click', 'Jinja2', 'jinja2-strcase', 'rich', 'GitPython'
      ])