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
                 object_regex = r'\d+', lookup_field = 'pk',
                 extra_context=None, template_object_name = 'object',
                 has_edit_permission = lambda request, obj: True,
                 context_processors=None):
        
        self.object_regex = object_regex
        self.lookup_field = lookup_field
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
        
        
    def get_object(self, *args, **kwargs):
        '''
        If one positioned argument is given it is used as
        a value for lookup with key=self.lookup_field ('pk'
        by default). If keyword arguments are given they are
        passed as queryset's get lookup parameters.
        '''
        if args and not kwargs:
            kwargs = {self.lookup_field: args[0]} 
            args = []           
        return self.queryset.get(*args, **kwargs)
        
        
    def get_object_or_404(self, *args, **kwargs):
        '''
        If one positioned argument is given it is used as
        a value for lookup with key=self.lookup_field ('pk'
        by default). If keyword arguments are given they are
        passed as queryset's get lookup parameters. If no object
        is found Http404 exception is raised. 
        '''
        try:
            return self.get_object(*args, **kwargs)                
        except self.queryset.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.queryset.model._meta.object_name)
    

    def get_common_context(self, object):
        context = {self.template_object_name: object, 'current_app': self.app_name}
        if (self.extra_context):
            context.update(self.extra_context)
        return context
    
    
    def get_object_and_context(self, *args, **kwargs):
        obj = self.get_object_or_404(*args, **kwargs)
        return obj, self.get_common_context(obj)
    
                    
    def make_regex(self, url):  
        ''' 
            Make regex string for ``PluggableSite`` urlpatterns: prepend url
            with parent object's url and app name.
            
            See also: http://code.djangoproject.com/ticket/11559.
        '''      
        return r"^(?P<object_id>%s)/%s%s$" % (self.object_regex, self.app_name, url)
    
    
    def patterns(self):
        ''' This method should return url patterns (like urlpatterns variable in 
            :file:`urls.py`). It is helpful to construct regex with
            :meth:`~generic_utils.app_utils.PluggableSite.make_regex` method.
            Example::
            
                return patterns('photo_albums.views',                                
                                    url(
                                        self.make_regex('/'),
                                        'show_album',
                                        {'album_site': self},
                                        name = 'show_album',
                                    ),
                               )
        '''
        
        raise NotImplementedError


    @property
    def urls(self):
        '''  
            Use it in :file:`urls.py`.
            Example::
            
                urlpatterns += patterns('', url(r'^my_site/', include(my_pluggable_site.urls)),)
        '''
        return self.patterns(), self.app_name, self.instance_name
