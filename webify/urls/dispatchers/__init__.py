from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from webob import exc, Request, Response

def PassThrough(controller):
    def dispatcher(environ, start_response):
        req = Request(environ) 
        # ignore url; path info
        relative_url = req.path_info
        responds_to_url = True
        if responds_to_url:
            return controller(environ, start_response)
        else:
            return exc.HTTPNotFound()(environ, start_response)
    return dispatcher


class Shifter(object):
    def __init__(self, default_controller):
        self.urls = []
        self.url_dict = None
        self.default_controller = default_controller

    def wrap(self, path=None, controller=None, url_args=None):
        def decorator(f, path=path):
            if path is None:
                path = f.func_name
            assert(f is not None)
            c = self.default_controller(f) if controller is None else controller(f)
            assert(c is not None)
            self.urls.append((path, url_args, c))
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


