#coding: utf-8

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from generic_utils.managers import GenericModelManager, GenericInjector

class GenericModelBase(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = GenericModelManager()
    injector = GenericInjector()

    class Meta:
        abstract=True
        

# untested
class TrueGenericModelBase(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    content_object = GenericForeignKey()

    objects = GenericModelManager()
    injector = GenericInjector()

    class Meta:
        abstract=True