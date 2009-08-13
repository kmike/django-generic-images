from django.db import models
from django.contrib.contenttypes.models import ContentType


class AttachedImageManager(models.Manager):
    ''' Manager with helpful functions for attached images
    '''
    def get_for_model(self, model):
        ''' Returns all images that are attached to given model '''
        content_type = ContentType.objects.get_for_model(model)
        images = self.get_query_set().filter(content_type=content_type, object_id=model.pk)
        return images
            
    def get_main_for(self, model):
        ''' Returns main image for given model '''
        try:
            return self.get_for_model(model).get(is_main=True)
        except models.ObjectDoesNotExist:
            return None
            
