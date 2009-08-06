#coding: utf-8
from django.conf.urls.defaults import *
from django.http import Http404
from django.core.urlresolvers import reverse
        

class PluggableSite(object):
    ''' Base class for reusable apps. 
        The approach is similar to django AdminSite.
        For usage case please check photo_albums app.
    '''
    def __init__(self, instance_name, queryset, app_name, 
                 extra_context=None, template_object_name = 'object',
                 has_edit_permission = lambda request, obj: True,
                 context_processors=None):
        self.instance_name = instance_name
        self.queryset = queryset
        self.extra_context = extra_context or {}
        self.app_name = app_name
        self.has_edit_permission = has_edit_permission
        self.template_object_name = template_object_name
        self.context_processors = context_processors
        
    def reverse(self, url, args=None, kwargs=None):
        ''' Reverse an url taking self.app_name in account '''
        return reverse("%s:%s" % (self.instance_name, url,), 
                        args=args,
                        kwargs=kwargs, 
                        current_app = self.app_name)
                
        
    def check_permissions(self, request, object):
        if not self.has_edit_permission(request, object):
            raise Http404('Not allowed')
        
        
    def get_object_or_404(self, object_id):        
        try:
            object = self.queryset.get(pk=object_id)
        except self.queryset.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.queryset.model._meta.object_name)
        return object
    

    def get_common_context(self, object):
        context = {self.template_object_name: object, 'current_app': self.app_name}
        if (self.extra_context):
            context.update(self.extra_context)
        return context
    
    
    def get_object_and_context(self, object_id):
        obj = self.get_object_or_404(object_id)
        return obj, self.get_common_context(obj)
        

    def patterns(self):
        ''' This method should return url patterns 
            (like urlpatterns variable in urls.py).
            Example::
            
            return patterns('photo_albums.views',                                
                                url(
                                    r'^(?P<object_id>\d+)/%s/$' % self.app_name,
                                    'show_album', 
                                    {'album_site': self},
                                    name = 'show_album',
                                ),
                           )
        '''
        
        raise NotImplementedError


    @property
    def urls(self):
        return self.patterns(), self.app_name, self.instance_name
