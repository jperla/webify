from __future__ import absolute_import
import types
import logging

from . import standard

from ..urls import defaults, dispatchers
from .. import http as _http
from .. import App


class DispatcherApp(App):
    def __init__(self, dispatcher=defaults.dispatcher):
        #TODO: jperla: should pass an object, not a class
        self.dispatcher = dispatcher()

    def __call__(self, req, p):
        assert(isinstance(req, _http.Request))
        app, req = self.dispatcher(req)
        return app(req, p)
        
    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.url = self._decorate_url(subapp, subapp.url)
            self.dispatcher.register(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def _decorate_url(self, subapp, suburl):
        def url_decorator(*args, **kwargs):
            url = self.dispatcher.url(subapp, suburl(*args, **kwargs))
            return url
        return url_decorator

class SingleApp(DispatcherApp):
    def __init__(self):
        DispatcherApp.__init__(self, dispatcher=dispatchers.SingleDispatcher)


