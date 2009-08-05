
from django.db import models
from django.contrib.contenttypes.models import ContentType


class GenericInjector(models.Manager):
    ''' Manager for selecting all generic-related objects in one (two) SQL queries.
        Selection is performed for a list of objects. Resulting data is aviable as attribute 
        of original model. Only one instance per object can be selected. Example usage: 
        select (and make acessible as user.avatar) all avatars for a list of user when 
        avatars are AttachedImage's attached to User model with is_main=True attributes.
    '''
    def inject_to(self, objects, field_name, get_inject_object = lambda obj: obj, **kwargs):
        try:
            content_type = ContentType.objects.get_for_model(get_inject_object(objects[0]))        
        except IndexError:
            return objects
        
        #get related data
        data = self.get_query_set().filter(content_type=content_type, 
                                           object_id__in=[ get_inject_object(object).pk for object in objects ],
                                           **kwargs)                
        data_dict = dict((item.object_id, item) for item in list(data))
        
        # add info to original data
        for object in objects:
            pk = get_inject_object(object).pk
            if data_dict.has_key(pk):
                get_inject_object(object).__setattr__(field_name, data_dict[pk])    
