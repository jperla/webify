from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from webob import exc, Request, Response


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


class UrlizedController(object):
    def __init__(self, controller, url_parser):
        self.controller = controller
        self.url_parser = url_parser
    
    def url(self, *args, **kwargs):
        return self.url_parser.url(*args, **kwargs)

    def __call__(self, environ, start_response):
        args, kwargs = self.url_parser.parse(environ)
        self.controller.append_args(args, kwargs)
        return self.controller(environ, start_response)
        
class RemainingParser(object):
    def __init__(self, prefix='/'):
        self.prefix = prefix

    def url(self, remaining):
        return self.prefix + remaining

    def parse(self, environ):
        path = environ['PATH_INFO']
        assert(path.startswith(self.prefix))
        remaining = path[len(self.prefix):]
        if remaining != '':
            args = [remaining]
        else:
            args = []
        kwargs = {}
        return (args, kwargs)

class RemainingMapper(object):
    def __init__(self, path=None):
        self.__path = path

    def path(self, f):
        return '/%s/' % f.func_name if self.__path is None else self.__path

    def map(self, f, controller):
        p = RemainingParser(self.path(f))
        c = controller(f)
        urlized = UrlizedController(c, p)
        return urlized 

    def slash(self, f):
        #TODO: jperla: not quite right
        return self.path(f).replace('/', '')

class SlashDispatcher(object):
    def __init__(self, default_controller):
        self.urls = []
        self.url_dict = None
        self.default_controller = default_controller

    def urlize(self, controller=None, mapper=RemainingMapper()):
        def decorator(f):
            assert(f is not None)
            c = self.default_controller if controller is None else controller
            assert(c is not None)
            urlized = mapper.map(f, c)
            slash = mapper.slash(f)
            assert(urlized is not None)
            self.urls.append((slash, mapper, urlized))
            return urlized 
        return decorator

    def app_for_name(self, name):
        if self.url_dict is None:
            self.__build_url_dict()
        return self.url_dict.get(name, (None, None))

    def __build_url_dict(self):
        self.url_dict = {}
        for name,mapper,controller in self.urls:
            self.url_dict[name] = (mapper, controller)


    def application(self):
        return self

    def __call__(self, environ, start_response):
        name = environ['PATH_INFO'].split('/')[1]
        if name is None:
            name = ''
        mapper, app = self.app_for_name(name)
        if app is None:
            res = webob.Response()
            res.status = 404
            return res(environ, start_response)
        else:
            return app(environ, start_response)
