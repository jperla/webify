from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from . import standard

from ..urls import defaults, dispatchers
from ..controllers import arguments
from .. import http as _http
from .. import Controller, CallableApp


class App(CallableApp):
    def __init__(self, dispatcher=defaults.dispatcher):
        self.dispatcher = dispatcher()
        self.superapp = None

    def __call__(self, environ, start_response):
        return self.dispatcher(environ, start_response)

    def controller(self, *args, **kwargs):
        def controller_wrapper(f):
            c = f if isinstance(f, Controller) else Controller(f)
            s = self.subapp(*args, **kwargs)(c)
            return s
        return controller_wrapper
        
    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.superapp = self
            subapp.__call__ = self._decorate_call(subapp.__call__)
            self.dispatcher.register(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def url(self, subapp, suburl):
        url = self.dispatcher.url(subapp, suburl)
        if self.superapp is not None:
            super_url = self.superapp.url(self, url)
        else:
            super_url = url
        return super_url

    def body(self, iterable):
        # Layouts here
        return iterable

    def _decorate_call(self, subapp_call):
        def call_decorator(environment, start_response):
            return subapp_call(environment, start_response)
        return call_decorator



class SimpleApp(App):
    def __init__(self):
        App.__init__(self, dispatcher=dispatchers.SingleDispatcher)


