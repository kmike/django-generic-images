#!/usr/bin/env python
from distutils.core import setup

setup(
      name='django-generic-images',
      version='0.14',
      author='Mikhail Korobov',
      author_email='kmike84@gmail.com',
      url='http://bitbucket.org/kmike/django-generic-images/',      
      
      description = 'Generic images pluggable django app',
      long_description = "This app provides image model (with useful managers etc) that can be attached to any other Django model using generic relations. ",
      license = 'MIT license',
      packages=['generic_images', 'generic_utils'],
      package_data={'generic_images': ['locale/en/LC_MESSAGES/*','locale/ru/LC_MESSAGES/*']},      
      
      classifiers=(
          'Development Status :: 3 - Alpha',
          'Environment :: Plugins',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Natural Language :: Russian',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules'
        ),
)