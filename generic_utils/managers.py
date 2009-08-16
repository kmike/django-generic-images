
from django.db import models
from django.contrib.contenttypes.models import ContentType


def _pop_data_from_kwargs(kwargs):
    try:
        ct_field = kwargs.pop('ct_field')
    except KeyError:
        ct_field = 'content_type'

    try:
        fk_field = kwargs.pop('fk_field')
    except KeyError:
        fk_field = 'object_id'

    return ct_field, fk_field
    

class GenericInjector(models.Manager):
    ''' Manager for selecting all generic-related objects in one (two) SQL queries.
        Selection is performed for a list of objects. Resulting data is aviable as attribute 
        of original model. Only one instance per object can be selected. Example usage: 
        select (and make acessible as user.avatar) all avatars for a list of user when 
        avatars are AttachedImage's attached to User model with is_main=True attributes.
    '''
    
    def __init__(self, *args, **kwargs):
        self.ct_field, self.fk_field = _pop_data_from_kwargs(kwargs)    
        super(GenericInjector, self).__init__(*args, **kwargs)
        
    
    def inject_to(self, objects, field_name, get_inject_object = lambda obj: obj, **kwargs):
        try:
            content_type = ContentType.objects.get_for_model(get_inject_object(objects[0]))        
        except IndexError:
            return objects
        
        #get related data
        kwargs.update({
                        self.ct_field: content_type, 
                        self.fk_field+'__in': [ get_inject_object(object).pk for object in objects ]
                     })
        data = self.get_query_set().filter(**kwargs)                
        data_dict = dict((getattr(item, self.fk_field), item) for item in list(data))
        
        # add info to original data
        for object in objects:
            pk = get_inject_object(object).pk
            if data_dict.has_key(pk):
                get_inject_object(object).__setattr__(field_name, data_dict[pk])    

    
    
class GenericModelManager(models.Manager):
    """ Manager with for_model method.  """    
    
    def __init__(self, *args, **kwargs):
        self.ct_field, self.fk_field = _pop_data_from_kwargs(kwargs)    
        super(GenericModelManager, self).__init__(*args, **kwargs)
    
    def for_model(self, model):
        ''' Returns all objects that are attached to given model '''
        content_type = ContentType.objects.get_for_model(model)
        kwargs = {
                    self.ct_field: content_type, 
                    self.fk_field: model.pk
                 }
        objects = self.get_query_set().filter(**kwargs)
        return objects
                    
                