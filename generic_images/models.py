#coding: utf-8
import os

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericTabularInline, GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from generic_utils.injector import GenericInjector


class ReplaceOldImageModel(models.Model):
    '''
        Abstract Model class with image field.
        If the file for image is re-uploaded, old file is deleted.
    '''
    
    def get_upload_path(self, filename):
        ''' Override this to customize upload path
        '''
        raise NotImplementedError

    def _upload_path_wrapper(self, filename):
        return self.get_upload_path(filename)

    image = models.ImageField(_('Image'), upload_to=_upload_path_wrapper)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_obj = self.__class__.objects.get(pk=self.pk)
                if old_obj.image.path != self.image.path:
                    path = old_obj.image.path
                    default_storage.delete(path)
            except self.__class__.DoesNotExist:
                pass
        super(ReplaceOldImageModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        
                                
        
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
        except AttachedImage.DoesNotExist:
            return None
            

class AttachedImage(ReplaceOldImageModel):
    '''
        Image model that can be attached to any other Django model using 
        generic relations. 
    '''
    
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_('User'))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    caption = models.TextField(_('Caption'), null=True, blank=True)
    is_main = models.BooleanField(_('Main image'), default=False)
    
    order = models.IntegerField(_('Order'), default=0)

    objects = AttachedImageManager()
    injector = GenericInjector()        
    
    
    def _get_next_pk(self):
        max_pk = AttachedImage.objects.aggregate(max_pk=Max('pk'))['max_pk'] or 0
        return max_pk+1
    
        
    def get_upload_path(self, filename):
        ''' Override this in proxy subclass to customize upload path.
            Default upload path is "/media/images/<user.id>/<image.id>.<ext>"
            or "/media/images/common/<image.id>.<ext>" if user is not set.
            image.id is predicted as it is unknown at this stage.
        '''        
        predicted_pk = self._get_next_pk()        
        user_folder = str(self.user.pk) if self.user else 'common'
        
        root, ext = os.path.splitext(filename)
        return os.path.join('media', 'images', user_folder, str(predicted_pk) + ext)    
    
    
    def save(self, *args, **kwargs):
        if self.is_main:
            related_images = AttachedImage.objects.filter(content_type=self.content_type, 
                                                          object_id=self.object_id)
            related_images.update(is_main=False)
        if not self.pk:
            self.order = self._get_next_pk()
        super(AttachedImage, self).save(*args, **kwargs)        
    
        
    def __unicode__(self):
        try:
            if self.user:
                return u"AttachedImage #%d for [%s] by [%s]" % (self.pk, self.content_object, self.user)
            else:
                return u"AttachedImage #%d for [%s]" % (self.pk, self.content_object,)
        except:
            try:
                return u"AttachedImage #%d" % (self.pk)
            except TypeError:
                return u"new AttachedImage"
            
            
    class Meta:
        ordering = ['-order']
        
        
class AttachedImageInline(GenericTabularInline):
    model = AttachedImage

