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
    ''' InlineModelAdmin for attached images.
        Adds multi-image uploader with progress bar, before-upload image
        previews and client-side resizing. Uploader is based
        on GearsUploader (http://bitbucket.org/kmike/gearsuploader/) project.

        To make this work copy ``generic_images`` folder from
        ``generic_images/media/`` to your ``MEDIA_ROOT``. Then use
        AttachedImagesInline class for you inlines::

            #admin.py

            from django.contrib import admin
            from generic_images.admin import AttachedImagesInline

            class MyModelAdmin(admin.ModelAdmin):
                inlines = [AttachedImagesInline]

            admin.site.register(MyModel, MyModelAdmin)


        Just before standard formset the following uploader is displayed:

        .. image:: img/admin-with-formset.png

        Gears plugin is here

        .. image:: img/admin-nogears.png

        Message is displayed if Gears plugin is not available

        .. image:: img/admin-previews.png

        User can select several files at once using Ctrl or Shift keys
        (Cmd on Mac) in standard OS file selection dialog. He can also remove
        images from selection by clicking on thumbnails. Several files can also
        be selected by opening file selection dialog several times.

        .. image:: img/admin-uploading.png

        User presses 'Upload' button and upload process begins


        By default the 'Resize ..' checkbox is unchecked and the input field is
        blank. If it is unchecked then images are not resized before uploading.
        User can check it and set his max image width.

        In order to set the default value and mark the checkbox as checked by
        default subclass AttachedImagesInline and set ``max_width`` parameter::

            class MyImagesInline(AttachedImagesInline):
                max_width=600

            class MyModelAdmin(admin.ModelAdmin):
                inlines = [MyImagesInline]

            admin.site.register(MyModel, MyModelAdmin)

    '''
    model = AttachedImage
    form = AttachedImageAdminForm
    template = 'generic_images/attached_images_inline.html'

#    max_width=600
