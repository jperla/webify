from __future__ import absolute_import
import types
import logging
import wsgiref

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
    def __init__(self):
        App.__init__(self)

    def __call__(self, req, p):
        app, req = self.dispatched_app_and_request(req, p)
        app(req, p)

    def dispatched_app_and_request(req, p):
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

    def wrap_url(self, subapp, suburl):
        url = self.parented_url(subapp, suburl)
        if self.parent is None:
            return url
        else:
            return self.parent.wrap_url(self, url)

    def parented_url(self, subapp, suburl):
        raise NotImplementedError

class SimpleDispatchApp(DispatchApp):
    def __init__(self, default=None):
        self.default = default
        self.apps, self.urls = {}, {}
    
    def default_subapp(self, *args, **kwargs):
        assert(self.default is None)
        def subapp_decorator(subapp):
            subapp.parent = self
            self.default = subapp
            return subapp
        return subapp_decorator

    def dispatched_app_and_request(self, req, p):
        path_info = req.environ[u'PATH_INFO'] #for debugging
        #TODO: jperla: deep copy request here?
        name = u'/%s' % req.path_info.lstrip('/').split('/', 1)[0]
        apps = self.apps
        app = apps.get(name, None)
        if app is not None:
            wsgiref.util.shift_path_info(req.environ)
            return app, req
        else:
            if self.default is not None:
                return self.default, req
            else:
                raise _http.status.not_found()

    def register_subapp(self, subapp, path=None):
        name = (u'/%s' % subapp.func.func_name) if path is None else path
        if name in self.apps:
            raise Exception(u'Already dispatching to path: %s' % path)
        self.apps[name] = subapp
        self.urls[subapp] = name

    def parented_url(self, subapp, suburl):
        assert(subapp in self.urls or subapp == self.default)
        #TODO: jperla: fix index urls
        if subapp == self.default:
            return suburl
        else:
            return (self.urls[subapp] + suburl).replace(u'//', u'/')

class BooleanDispatchApp(DispatchApp):
    def __init__(self, default=None):
        self.default = default
        self.apps = {}
        DispatchApp.__init__(self)

    def dispatched_app_and_request(self, req, p):
        path_info = req.environ[u'PATH_INFO'] #for debugging
        apps = self.apps
        for boolean, subapp in apps.iteritems():
            if boolean(req):
                return subapp, req
        if self.default is not None:
            return self.default, req
        else:
            raise _http.status.not_found()

    def register_subapp(self, subapp, boolean):
        if boolean in self.apps:
            raise Exception(u'Already dispatching to path: %s' % path)
        self.apps[boolean] = subapp

    def parented_url(self, subapp, suburl):
        assert(subapp in self.apps.values())
        return suburl

class SingleApp(DispatcherApp):
    def __init__(self):
        DispatcherApp.__init__(self, dispatcher=dispatchers.SingleDispatcher)


