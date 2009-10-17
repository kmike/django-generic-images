from django import forms
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

from generic_images.models import AttachedImage

admin.site.register(AttachedImage)

class AttachedImageAdminForm(forms.ModelForm):
    ''' Form for AttachedImage model to be used in inline admin '''

    caption = forms.CharField(label=_('Caption'), required=False)

    class Media:
        js = [
              'generic_images/js/mootools-1.2.3-core-yc.js',
              'generic_images/js/GearsUploader.en.yui.js',
              'generic_images/js/AttachedImageInline.js',
        ]
    class Meta:
        model = AttachedImage


class AttachedImagesInline(GenericTabularInline):
    ''' InlineAdmin for attached images.
        Adds multi-image uploader with progress bar, before-upload image
        previews and client-side resizing. Uploader is based
        on GearsUploader project.

        By default images are not resized. In order to enable resizing
        subclass AttachedImageInline and set ``max_width`` parameter::

            class MyImageInline(AttachedImagesInline):
                max_width=600

    '''
    model = AttachedImage
    form = AttachedImageAdminForm
    template = 'generic_images/attached_images_inline.html'

#    max_width=600
