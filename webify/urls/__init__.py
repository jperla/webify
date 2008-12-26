from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

from ..controllers import IncrementalController

class UrlWrapper(object):
    class Arguments(object):
        class Path(object):
            def __init__(self):
                pass

            def __call__(self, controller, environ, start_response):
                args = environ['PATH_INFO'].split('/', 1)
                if len(args) <= 1:
                    path = None
                else:
                    path = args[1]
                #TODO: jperla: looks ugly; must be something better
                if path is None:
                    raise Exception('Error parsing url: %s' % environ['PATH_INFO'])
                controller.append_args(path)
                return controller(environ, start_response)

    def __init__(self, default_controller=IncrementalController):
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


