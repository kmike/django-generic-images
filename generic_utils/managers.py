
from django.db import models
from django.contrib.contenttypes.models import ContentType

from generic_images.models import AttachedImage
                
                
class ImagesAndUserManager(models.Manager):
    
    def select_with_main_images(self, limit=None, **kwargs):
        ''' Select all objects with filters passed as kwargs.   
            For each object it's main image instance is accessible as ``object.main_image``.
            Results can be limited using ``limit`` parameter.
            Selection is performed using only 2 or 3 sql queries.            
        '''
        objects = self.get_query_set().filter(**kwargs)[:limit]
        AttachedImage.injector.inject_to(objects,'main_image', is_main=True)
        return objects
    
    def for_user_with_main_images(self, user, limit=None):
        return self.select_with_main_images(user=user, limit=limit)
            
    def get_for_user(self, user):
        objects = self.get_query_set().filter(user=user)
        return objects
                            
