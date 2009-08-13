#coding: utf-8
import os
import random

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericTabularInline, GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from generic_utils.injector import GenericInjector
from generic_images.signals import image_saved, image_deleted
from generic_images.managers import AttachedImageManager


class BaseImageModel(models.Model):
    ''' Simple abstract Model class with image field.
    '''
    
    def get_upload_path(self, filename):
        ''' Override this to customize upload path
        '''
        raise NotImplementedError

    def _upload_path_wrapper(self, filename):
        return self.get_upload_path(filename)

    image = models.ImageField(_('Image'), upload_to=_upload_path_wrapper)
    
    class Meta:
        abstract = True



class ReplaceOldImageModel(BaseImageModel):
    '''
        Abstract Model class with image field.
        If the file for image is re-uploaded, old file is deleted.
    '''
    
    def _replace_old_image(self):
        ''' Override this in subclass if you don't want
            image replacing or want to customize image replacing
        '''
        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            if old_obj.image.path != self.image.path:
                path = old_obj.image.path
                default_storage.delete(path)
        except self.__class__.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if self.pk:
            self._replace_old_image()
        super(ReplaceOldImageModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        
                                
        

class AbstractAttachedImage(ReplaceOldImageModel):
    '''
        Abstract Image model that can be attached to any other Django model using 
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
        max_pk = self.__class__.objects.aggregate(max_pk=Max('pk'))['max_pk'] or 0
        return max_pk+1


    def get_file_name(self, filename):
#        alphabet = "1234567890abcdefghijklmnopqrstuvwxyz"        
#        return ''.join([random.choice(alphabet) for i in xrange(16)]) # 1e25 variants
        return str(self._get_next_pk()) # anyway _get_next_pk is needed for setting `order` field
    
        
    def get_upload_path(self, filename):
        ''' Override this in proxy subclass to customize upload path.
            Default upload path is "/media/images/<user.id>/<image.id>.<ext>"
            or "/media/images/common/<image.id>.<ext>" if user is not set.
            image.id is predicted as it is unknown at this stage.
        '''        
        user_folder = str(self.user.pk) if self.user else 'common'        
        
        root, ext = os.path.splitext(filename)
        return os.path.join('media', 'images', user_folder, self.get_file_name(filename) + ext)    
    
    
    def save(self, *args, **kwargs):
        if self.is_main:
            related_images = self.__class__.objects.filter(content_type=self.content_type, 
                                                          object_id=self.object_id)
            related_images.update(is_main=False)
        if not self.pk:
            self.order = self._get_next_pk()
        super(AbstractAttachedImage, self).save(*args, **kwargs)         
        image_saved.send(sender = self.content_type.model_class(), instance = self)
        
        
    def delete(self, *args, **kwargs):
        image_deleted.send(sender = self.content_type.model_class(), instance = self)
        super(AbstractAttachedImage, self).delete(*args, **kwargs)            
        
        
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
        abstract=True
        


class AttachedImage(AbstractAttachedImage):
    '''
        Image model that can be attached to any other Django model using 
        generic relations.
    '''    
    class Meta:
        ordering = ['-order']


class AttachedImageInline(GenericTabularInline):
    model = AttachedImage

