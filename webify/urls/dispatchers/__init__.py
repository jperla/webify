from __future__ import absolute_import
import wsgiref
import wsgiref.util

from ... import http


class SimpleDispatcher(object):
    def __init__(self):
        self.apps, self.urls = {}, {}

    def register(self, subapp, path=None):
        name = ('/%s' % subapp.func.func_name) if path is None else path
        if name in self.apps:
            raise Exception('Already dispatching to path: %s' % path)
        self.apps[name] = subapp
        self.urls[subapp] = name

    def url(self, subapp, controller_url):
        assert(subapp in self.urls)
        #TODO: jperla: fix index urls
        return (self.urls[subapp] + controller_url).replace('//', '/')

    def __call__(self, environ, start_response):
        path_info = environ['PATH_INFO'] #for debugging
        name = wsgiref.util.shift_path_info(environ)
        if name is None:
            name = ''
        name = '/%s' % name
        apps = self.apps
        app = apps.get(name)
        if app is not None:
            return app(environ, start_response)
        else:
            raise http.status.not_found()

class SingleDispatcher(object):
    def __init__(self):
        self.subapp = None

    def register(self, subapp):
        assert(subapp is not None)
        if self.subapp is not None:
            raise Exception('Single dispatcher only dispatches '
                            'to one controller')
        else:
            self.subapp = subapp

    def url(self, subapp, controller_url):
        assert(subapp == self.subapp)
        return '%s' % controller_url

    def __call__(self, environ, start_response):
        app = self.subapp
        if app is not None:
            return app(environ, start_response)
        else:
            raise http.status.not_found()

