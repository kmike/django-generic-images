.. django-generic-images documentation master file, created by
   sphinx-quickstart on Fri Sep 18 02:13:39 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
.. toctree::
   :maxdepth: 2
   
=====================================   
django-generic-images's documentation
=====================================

django-generic-images is a generic images pluggable django app.

This app provides image model (with useful managers, methods and fields) 
that can be attached to any other Django model using generic relations.

Requirements: django 1.1 (or trunk).

django-composition is required if you want to use ImageCountField or 
UserImageCountField.

************
Installation
************
::

	$ easy_install django-generic-images
	
or::

	$ hg clone http://bitbucket.org/kmike/django-generic-images/ 
	$ cd django-generic-images
	$ python setup.py install

Then add 'generic_images' to your INSTALLED_APPS in settings.py and run ::

	$ manage.py syncdb

For django-composition installation follow instructions at 
http://bitbucket.org/daevaorn/django-composition/src/

*****
Usage
*****

Generic Images
==============

Models
------

.. automodule:: generic_images.models
	:exclude-members: Meta, save, delete
	:show-inheritance:
	:members:
	:undoc-members:


Forms
-----

.. automodule:: generic_images.forms
	:members:
	
Fields for denormalisation
--------------------------

.. automodule:: generic_images.fields
	:members:
	

Context processors
------------------

.. automodule:: generic_images.context_processors
	:members:
	
	
Generic Utils
=============	

Pluggable app utils
-------------------	
.. automodule:: generic_utils.app_utils
	:members:
	:undoc-members:

	
Generic relation helpers
------------------------

.. automodule:: generic_utils.managers
	:members:
	:undoc-members:
		
	

Template tag helpers
--------------------
	
.. automodule:: generic_utils.templatetags
	:members:
	:undoc-members:
		

Test helpers
------------

.. automodule:: generic_utils.test_helpers
	:members:
			