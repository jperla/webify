from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from webob import exc, Request, Response
from .. import mappers
from ... import http


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
    def __init__(self, default_controller, default_mapper):
        self.apps = {}
        self.default_controller = default_controller
        self.default_mapper = default_mapper

    def urlize(self, controller=None, mapper=None):
        mapper = self.default_mapper if mapper is None else mapper
        assert(isinstance(mapper, mappers.HashMapper),
                'Slash Dispatcher uses a hash mapping system')
        def decorator(f):
            assert(f is not None)
            c = self.default_controller if controller is None else controller
            assert(c is not None)
            urlized_controller = mapper.map(f, c)
            assert(urlized_controller is not None)
            key = mapper.key(f)
            self.apps[key] = urlized_controller
            return urlized_controller
        return decorator

    def __call__(self, environ, start_response):
        name = environ['PATH_INFO'].split('/')[1]
        if name is None:
            name = ''
        app = self.apps.get(name, None)
        if app is not None:
            return app(environ, start_response)
        else:
            raise http.status.not_found()

