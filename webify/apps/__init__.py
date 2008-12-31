from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from ..urls import defaults
from ..controllers import arguments
from .. import http as _http

        
def get_req(environ):
    req = Request(environ)
    if 'settings' not in req.environ or req.environ['settings'] == []:
        req.settings = {} 
    else:
        req.settings = req.environ['settings'][0] 
    return req


def recursively_iterate(g):
    for item in g:
        if not hasattr(item, '__iter__'):
            yield item
        else:
            for subitem in recursively_iterate(item):
                yield subitem

def Url(object):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

class CallableApp(object):
    def __init__(self, func):
        raise NotImplementedError

    def __call__(self, environ, start_response):
        raise NotImplementedError

class Controller(CallableApp):
    def __init__(self, func):
        self.func = func
        self.arg_parsers = []

    def url(self, *args, **kwargs):
        url_arg_parser = None
        for parser in self.arg_parsers:
            if isinstance(parser, arguments.UrlArgParser):
                url_arg_parser = parser
                break
        if url_arg_parser is None:
            return '/'
        else:
            return url_arg_parser.url(*args, **kwargs)
    
    def __call__(self, environ, start_response):
        req = get_req(environ)
        args, kwargs = [], {}
        for parser in self.arg_parsers:
            parser_args, parser_kwargs = parser.parse(req)
            args.extend(parser_args)
            kwargs.update(parser_kwargs)
        try:
            resp_generator = self.func(req, *args, **kwargs)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = _http.defaults.status_and_headers
            first_yield = resp_generator.next()
            if not isinstance(first_yield, exc.HTTPException):
                start_response(status, headers)
                return recursively_iterate([first_yield, resp_generator])
            else:
                return first_yield(environ, start_response)

class App(CallableApp):
    def __init__(self, dispatcher=defaults.dispatcher):
        self.dispatcher = dispatcher()

    def __call__(self, environ, start_response):
        return self.dispatcher(environ, start_response)

    def controller(self, path=None, args=list()):
        def controller_wrapper(f):
            c = Controller(f)
            a = arguments.Arguments(*args)(c)
            if path is None:
                s = self.subapp()(a)
            else:
                s = self.subapp(path=path)(a)
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

