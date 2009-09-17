
from django.db import models
from django.contrib.contenttypes.models import ContentType


def _pop_data_from_kwargs(kwargs):
    ct_field = kwargs.pop('ct_field', 'content_type')
    fk_field = kwargs.pop('fk_field', 'object_id')
    return ct_field, fk_field
    

class GenericInjector(models.Manager):
    ''' Manager for selecting all generic-related objects in one (two) SQL queries.
        Selection is performed for a list of objects. Resulting data is aviable as attribute 
        of original model. Only one instance per object can be selected. Example usage: 
        select (and make acessible as user.avatar) all avatars for a list of user when 
        avatars are AttachedImage's attached to User model with is_main=True attributes.
        
        Example::

            from django.contrib.auth.models import User
            from generic_images.models import AttachedImage
            
            users = User.objects.all()[:10]
            AttachedImage.injector.inject_to(users, 'avatar', is_main=True)    

            # i=0..9: users[i].avatar is AttachedImage objects with is_main=True. 
            # If there is no such AttachedImage (user doesn't have an avatar), 
            # users[i].avatar is None


        For this example 2 or 3 sql queries will be executed:
            1. one query for selecting 10 users,
            2. one query for selecting all avatars (images with is_main=True) for selected users
            3. and maybe one query for selecting content-type for User model

One can reuse GenericInjector manager for other models that are supposed to 
be attached via generic relationship. It can be considered as an addition to 
GFKmanager and GFKQuerySet from djangosnippets for different use cases.
        
    '''
    
    def __init__(self, *args, **kwargs):
        self.ct_field, self.fk_field = _pop_data_from_kwargs(kwargs)    
        super(GenericInjector, self).__init__(*args, **kwargs)
        
    
    def inject_to(self, objects, field_name, get_inject_object = lambda obj: obj, **kwargs):
        '''        
        ``objects`` is an iterable. Images (or other generic-related model instances) 
            will be attached to elements of this iterable.
        
        ``field_name`` is the attached object attribute name
        
        ``get_injector_object`` is a callable that takes object in `objects` iterable.
            Image will be available as an attribute of the result of 
            `get_injector_object(object)`. Images attached to `get_injector_object(object)`
            will be selected.
        
        All other kwargs will be passed as arguments to queryset filter function.
        
        Example: you have a list of comments. Each comment has 'user' attribute. 
        You want to fetch 10 comments and their authors with avatars. Avatars should 
        be accessible as `user.avatar`::
        
            comments = Comment.objects.all().select_related('user')[:10]
            AttachedImage.injector.inject_to(comments, 'avatar', lambda obj: obj.user, is_main=True)   
        
        '''
        
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
                    
                