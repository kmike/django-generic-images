#coding: utf-8

from django.forms import ModelForm
from generic_images.models import AttachedImage


class AttachedImageForm(ModelForm):    
    ''' Basic form for AttachedImage model '''
    
    class Meta:
        model = AttachedImage
        fields = ['image', 'caption']
        
