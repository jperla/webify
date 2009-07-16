from __future__ import absolute_import
import types
import logging

from . import standard

from ..urls import defaults, dispatchers
from .. import http as _http
from .. import App

class PrefixApp(App):
    def __init__(self, subapp, prefix):
        App.__init__(self)
        self.prefix = prefix
        self.subapp = subapp
    
    def wrap_url(self, suburl):
        url = self.prefix + suburl
        if self.parent is None:
            return url
        else:
            return self.parent.wrap_url(url)

    def __call__(self, req, p):
        assert(req.environ[u'PATH_INFO'].startswith(self.prefix))
        req.environ[u'PATH_INFO'] = req.environ[u'PATH_INFO'][len(self.prefix):]
        self.subapp(req, p)


class DispatcherApp(App):
    def __init__(self, dispatcher=defaults.dispatcher):
        App.__init__(self)
        #TODO: jperla: should pass an object, not a class
        self.dispatcher = dispatcher()

    def __call__(self, req, p):
        assert(isinstance(req, _http.Request))
        app, req = self.dispatcher(req)
        return app(req, p)
        
    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.parent = self
            return subapp
        return subapp_decorator

class SingleApp(DispatcherApp):
    def __init__(self):
        DispatcherApp.__init__(self, dispatcher=dispatchers.SingleDispatcher)


