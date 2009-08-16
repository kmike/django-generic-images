
from django.db import models
from django.contrib.contenttypes.models import ContentType

    
class GenericModelManager(models.Manager):
    """ Manager with for_model method.  """    
    
    def __init__(self, ct_field="content_type", fk_field="object_id"):
        self.ct_field = ct_field
        self.fk_field = fk_field
    
    def for_model(self, model):
        ''' Returns all objects that are attached to given model '''
        content_type = ContentType.objects.get_for_model(model)
        kwargs = {
                    self.ct_field: content_type, 
                    self.fk_field: model.pk
                 }
        objects = self.get_query_set().filter(**kwargs)
        return objects
                    
                