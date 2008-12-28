from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from webob import exc, Request, Response
from .. import mappers


# potential problem: url parser and url dispatchers could conflict
# in the way that they parse the url

def Single(object):
    def __init__(self, default_controller):
        self.urls = []
        self.url_dict = None
        self.default_controller = default_controller

    def urlize(self):
        def decorator(f):
            c = self.default_controller(f)
            return c
        return decorator

    def application(self):
        return self

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        self.default_controller.append_args([path], {})
        return self.default_controller(environ, start_response)



class SlashDispatcher(object):
    def __init__(self, default_controller):
        self.urls = {}
        self.default_controller = default_controller

    def urlize(self, controller=None, mapper=mappers.RemainingMapper()):
        def decorator(f):
            assert(f is not None)
            c = self.default_controller if controller is None else controller
            assert(c is not None)
            urlized = mapper.map(f, c)
            key = mapper.key(f)
            assert(urlized is not None)
            self.urls[key] = (mapper, urlized)
            return urlized 
        return decorator

    def __call__(self, environ, start_response):
        name = environ['PATH_INFO'].split('/')[1]
        if name is None:
            name = ''
        mapper, app = self.urls.get(name, (None, None))
        if app is None:
            raise
            res = webob.Response()
            res.status = 404
            return res(environ, start_response)
        else:
            return app(environ, start_response)

