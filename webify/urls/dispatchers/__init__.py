from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from webob import exc, Request, Response

def Url(object):
    def __init__(self):
        pass

    def __str__(self):
        return ''

def UrlizedController(object):
    def __init__(self, controller, url_args):
        pass
    
    def url(self):
        pass

def Single(object):
    def __init__(self, default_controller):
        self.urls = []
        self.url_dict = None
        self.default_controller = default_controller

    def wrap(self):
        def decorator(f):
            c = self.default_controller(f)
            return c
        return decorator

    def application(self):
        return self

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        self.default_controller.append_args(path)
        return self.default_controller(environ, start_response)

class Shifter(object):
    def __init__(self, default_controller):
        self.urls = []
        self.url_dict = None
        self.default_controller = default_controller

    def wrap(self, path=None, controller=None, url_args=None):
        def decorator(f, path=path):
            assert(f is not None)
            if path is None:
                path = f.func_name
            c = self.default_controller(f) if controller is None else controller(f)
            assert(c is not None)
            self.urls.append((path, url_args, c))
            return c
        return decorator

    def app_for_name(self, name):
        if self.url_dict is None:
            self.__build_url_dict()
        return self.url_dict.get(name, (None, None))

    def __build_url_dict(self):
        self.url_dict = {}
        for name,url_args,controller in self.urls:
            self.url_dict[name] = (url_args, controller)


    def application(self):
        return self

    def __call__(self, environ, start_response):
        name = wsgiref.util.shift_path_info(environ)
        if name is None:
            name = ''
        url_args, app = self.app_for_name(name)
        if app is None:
            res = webob.Response()
            res.status = 404
            return res(environ, start_response)
        if url_args is not None:
            return url_args(app, environ, start_response)
        else:
            return app(environ, start_response)


