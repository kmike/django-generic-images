#coding: utf-8
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from composition.base import CompositionField
from generic_images.models import AttachedImage
from generic_images.signals import image_saved, image_deleted

        
class ImageCountField(CompositionField):
    ''' Field with model's attached images count.
        Value of this field is updated automatically when 
        image is added or removed. Access to this field
        doesn't produce additional 'select count(*)' query,
        data is stored in table.    
    '''
    def __init__(self, native=None):
                        
        self.internal_init(
            native = native or models.PositiveIntegerField(default=0, editable=False),
            trigger = {
                'on': (image_saved, image_deleted,),
                'do': lambda model, image, signal: AttachedImage.objects.get_for_model(model).count(),
                'field_holder_getter': lambda image: image.content_object
            }
        )        


class UserImageCountField(CompositionField):
    """ Field that should be put into user's profile (AUTH_PROFILE_MODULE). 
        It will contain number of images that are attached to corresponding User.
    """
    def __init__(self, native=None, user_attr='user'):                        
        
        def get_field_value(model, image, signal):
            return AttachedImage.objects.get_for_model(getattr(model, user_attr)).count()
        
        self.internal_init(
            native = native or models.PositiveIntegerField(default=0, editable=False),
            trigger = {
                'on': (image_saved, image_deleted,),
                'do': get_field_value,
                'field_holder_getter': lambda image: image.content_object.get_profile(),
                'sender_model': User,
            }
        )        
        
#class ImageCountField(CompositionField):
#    def __init__(self, native=None, signal=None):
#        
#        def get_field_value(model, image, signal):
##             we need to handle situation where the field with same name exists in model
##             but it is not this ImageCountField
#            if model is None:
#                return
#            ctype = ContentType.objects.get_for_model(self._composition_meta.model)
#            model_ctype = ContentType.objects.get_for_model(model)                        
#            if ctype==model_ctype:
#                try:
#                    return AttachedImage.objects.get_for_model(model).count()
#                except AttributeError:
#                    return None
#            else:
#                return 0
#                return getattr(model, self._composition_meta.name)
#        
#        self.internal_init(
#            native = native or models.PositiveIntegerField(default=0),
#            trigger = dict(
#                on = signal or (models.signals.post_save, models.signals.post_delete),
#                sender_model = AttachedImage,
#                do = get_field_value,
#                field_holder_getter = lambda image: image.content_object
#            )
#        )
#        
