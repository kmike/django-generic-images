
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.test.testcases import urlsplit, urlunsplit


class ViewTest(TestCase):
    '''
    TestCase for view testing
    '''
            
    def setUp(self):
        """This method is automatically called by the Django test framework."""
        self.client = Client()

    def check_url(self, url_name, status=200, kwargs=None, current_app=None):
        """check_url a URL and require a specific status code before proceeding"""
        response = self.client.get(reverse(url_name, kwargs=kwargs, current_app=current_app))
        self.failUnlessEqual(response.status_code, status)
        return response
    
    def check_login_required(self, url_name, login_url = '/accounts/login/', kwargs=None, current_app=None):
        """ Check if response is a redirect to login page (ignoring GET variables) """
        response = self.client.get(reverse(url_name, kwargs=kwargs, current_app=current_app))
        
        #remove GET variables, for example '?next=..'
        scheme, netloc, path, query, fragment = urlsplit(response['Location'])
        response['Location'] = urlunsplit(('http', 'testserver', path, None, None))
                
        self.assertRedirects(response, login_url)
        return response