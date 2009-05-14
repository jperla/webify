from __future__ import absolute_import
import types
import logging

from . import standard

from ..urls import defaults, dispatchers
from .. import http as _http
from .. import Controller, CallableApp


class App(CallableApp):
    def __init__(self, dispatcher=defaults.dispatcher):
        #TODO: jperla: should pass an object, not a class
        self.dispatcher = dispatcher()
        self.superapp = None
        self.layout = None

    def __call__(self, environ, start_response):
        if self.superapp is not None:
            resp_iterator = self.dispatcher(environ, start_response)
            return resp_iterator
        else:
            try:
                resp_iterator = self.dispatcher(environ, start_response)
            except _http.status.HTTPController, e:
                resp = e
                return resp(environ, start_response)
            else:
                return resp_iterator


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
        q = []
        if self.layout is None:
            q = iterable
        else:
            q = self.layout(iterable)
        if self.superapp is None:
            return output_encoding(recursively_iterate(q), u'utf-8')
        else:
            return q

    def _decorate_call(self, subapp_call):
        def call_decorator(environment, start_response):
            return subapp_call(environment, start_response)
        return call_decorator


#TODO: jperla: trash this shit
def recursively_iterate(item):
    if isinstance(item, unicode):
        yield item
    elif isinstance(item, str):
        raise Exception(u'Always work with unicode within your app!')
    else:
        for subitem in item:
            for i in recursively_iterate(subitem):
                yield i
def output_encoding(strings, encoding):
    for s in strings:
        encoded = s.encode(encoding)
        yield encoded


class SingleApp(App):
    def __init__(self):
        App.__init__(self, dispatcher=dispatchers.SingleDispatcher)


