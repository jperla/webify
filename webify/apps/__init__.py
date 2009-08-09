from __future__ import absolute_import
import types
import logging

from . import standard

from ..urls import defaults, dispatchers
from .. import http as _http
from .. import App

class PrefixApp(App):
    def __init__(self, subapp, prefix):
        self.prefix = prefix
        self.subapp = subapp
        self.subapp.parent = self
        App.__init__(self)
    
    def wrap_url(self, subapp, suburl):
        assert(self.subapp == subapp)
        url = self.prefix + suburl
        if self.parent is None:
            return url
        else:
            return self.parent.wrap_url(self, url)

    def __call__(self, req, p):
        assert(req.environ[u'PATH_INFO'].startswith(self.prefix))
        req.environ[u'PATH_INFO'] = req.environ[u'PATH_INFO'][len(self.prefix):]
        self.subapp(req, p)


class DispatcherApp(App):
    def __init__(self, dispatcher=defaults.dispatcher):
        #TODO: jperla: should pass an object, not a class
        self.dispatcher = dispatcher()
        App.__init__(self)

    def __call__(self, req, p):
        assert(isinstance(req, _http.Request))
        app, req = self.dispatcher(req)
        return app(req, p)
        
    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.parent = self
            self.dispatcher.register(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def wrap_url(self, subapp, suburl):
        url = self.dispatcher.url(subapp, suburl)
        if self.parent is None:
            return url
        else:
            return self.parent.wrap_url(self, url)

class DispatchApp(App):
    def __init__(self)
        raise NotImplementedError

    def __call__(self, req, p):
        # returns (app, req)
        raise NotImplementedError
        
    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.parent = self
            self.register_subapp(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def register_subapp(self, subapp):
        raise NotImplementedError

    def parent_url(self, subapp, suburl):
        url = self.wrap_url(subapp, suburl)
        if self.parent is None:
            return url
        else:
            return self.parent.parent_url(self, url)

    def wrap_url(self, subapp, suburl):
        raise NotImplementedError

class SimpleDispatchApp(DispatchApp):
    def __init__(self, default=None)
        self.default = None
        self.apps, self.urls = {}, {}

    def __call__(self, req, p):
        path_info = req.environ[u'PATH_INFO'] #for debugging
        #TODO: jperla: deep copy request here?
        name = u'/%s' % (wsgiref.util.shift_path_info(req.environ) or u'')
        apps = self.apps
        app = apps.get(name, None)
        if app is not None:
            return app, req
        else:
            if self.default is not None:
                return self.default, req
            else:
                raise http.status.not_found()

    def register_subapp(self, subapp, path=None):
        name = (u'/%s' % subapp.func.func_name) if path is None else path
        if name in self.apps:
            raise Exception(u'Already dispatching to path: %s' % path)
        self.apps[name] = subapp
        self.urls[subapp] = name

    def wrap_url(self, subapp, suburl):
        assert(subapp in self.urls or subapp == self.default)
        #TODO: jperla: fix index urls
        return (self.urls[subapp] + controller_url).replace(u'//', u'/')

class BooleanDispatchApp(DispatchApp):
    def __init__(self)
        self.apps = {}

    def __call__(self, req, p):
        path_info = req.environ[u'PATH_INFO'] #for debugging
        apps = self.apps
        for boolean, subapp in apps.iteritems():
            if boolean(path_info):
                return subapp, req
        # Otherwise, no matches
        raise http.status.not_found()

    def register_subapp(self, subapp, boolean):
        if boolean in self.apps:
            raise Exception(u'Already dispatching to path: %s' % path)
        self.apps[boolean] = subapp

    def wrap_url(self, subapp, suburl):
        assert(subapp in self.apps.values())
        #TODO: jperla: fix index urls
        return controller_url

class SingleApp(DispatcherApp):
    def __init__(self):
        DispatcherApp.__init__(self, dispatcher=dispatchers.SingleDispatcher)


