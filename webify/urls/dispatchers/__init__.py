from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from webob import exc, Request, Response
from ... import http
from ... import controllers



class SimpleDispatcher(object):
    def __init__(self):
        self.apps = {}
        self.urls = {}

    def urlize(self, path=None):
        def decorator(controller):
            assert(controller is not None)
            name = ('/%s' % controller.func.func_name) if path is None else path
            self.apps[name] = controller
            self.urls[controller] = name
            return controller
        return decorator

    def url(self, controller, controller_url):
        assert(controller in self.urls)
        return self.urls[controller] + controller_url

    def __call__(self, environ, start_response):
        path_info = environ['PATH_INFO'] #for debugging
        name = wsgiref.util.shift_path_info(environ)
        if name is None:
            name = ''
        name = '/%s' % name
        app = self.apps.get(name)
        if app is not None:
            return app(environ, start_response)
        else:
            raise http.status.not_found()

class SingleDispatcher(object):
    def __init__(self):
        self.controller = None

    def urlize(self):
        def decorator(controller):
            assert(controller is not None)
            self.controller = controller
            return controller
        return decorator

    def url(self, controller, controller_url):
        assert(controller == self.controller)
        return '/%s' % controller_url

    def __call__(self, environ, start_response):
        app = self.controller
        if app is not None:
            return app(environ, start_response)
        else:
            raise http.status.not_found()

