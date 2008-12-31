from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from . import standard

from ..urls import defaults
from ..controllers import arguments
from .. import http as _http
from .. import Controller, CallableApp


class App(CallableApp):
    def __init__(self, dispatcher=defaults.dispatcher):
        self.dispatcher = dispatcher()

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
            if isinstance(subapp, Controller):
                subapp.url = self._decorate_url(subapp, subapp.url)
            elif isinstance(subapp, App):
                subapp.decorate_url = self._decorate_decorate_url(subapp.decorate_url)
            self.dispatcher.register(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def _decorate_call(self, subapp_call):
        # Template goes here
        def call_decorator(environment, start_response):
            return subapp_call(environment, start_response)
        return call_decorator

    def _decorate_decorate_url(self, subapp_decorate_url):
        def decorate_url_decorator(subsubapp):
            url_decorator = subapp_decorate_url(subsubapp)
            def url_decorator_decorator(*args, **kwargs):
                suburl = url_decorator(*args, **kwargs)
                url = self.dispatcher.url(subsubapp, suburl)
                return url
            return url_decorator_decorator
        return decorate_url_decorator
        
        
    def _decorate_url(self, controller, controller_url):
        def url_decorator(*args, **kwargs):
            suburl = controller_url(*args, **kwargs)
            url = self.dispatcher.url(controller, suburl)
            return url
        return url_decorator

