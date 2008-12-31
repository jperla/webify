from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from . import arguments
from .. import http as _http

class CallableApp(object):
    def __init__(self, func):
        raise NotImplementedError

    def __call__(self, environ, start_response):
        raise NotImplementedError

def Url(object):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

class Controller(object):
    def __init__(self):
        pass

class Controller2(CallableApp):
    def __init__(self, func):
        self.func = func
        self.arg_parsers = []

    def url(*args, **kwargs):
        url_arg_parser = None
        for parser in self.arg_parsers:
            if isinstance(parser, UrlArgParser):
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

def App2(CallableApp):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, environ, start_response):
        return self.dispatcher(environ, start_response)
        
    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.superapp = self
            subapp.__call__ = self.decorate_call(subapp)
            if isinstance(subapp, Controller2):
                subapp.url = self.decorate_url(subapp)
            elif isinstance(subapp, App2):
                subapp.decorate_url = self.decorate_decorate_url(subapp)
            self.dispatcher.register(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def decorate_call(self, subapp):
        # Template goes here
        def call_decorator(environment, start_response):
            return subapp(environment, start_response)
        return call_decorator

    def decorate_decorate_url(self, subapp):
        def decorate_url_decorator(subsubapp):
            url_decorator = subapp.decorate_url(subsubapp)
            def url_decorator_decorator(*args, **kwargs):
                suburl = url_decorator(*args, **kwargs)
                url = self.dispatcher.url(controller, suburl)
                return url
            return url_decorator_decorator
        return decorate_url_decorator
        
        
    def decorate_url(self, controller):
        def url_decorator(*args, **kwargs):
            suburl = controller.url(*args, **kwargs)
            url = self.dispatcher.url(controller, suburl)
            return url
        return url_decorator


class ControllerWithArguments(Controller):
    def __init__(self, func):
        self.func = func
        self.args = list()
        self.kwargs = {}
        self.arg_parsers = (list(), {})

    def arg_parsers(self, *args, **kwargs):
        self.arg_parsers = (args, kwargs)

    def append_args(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def url(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, environ, start_response):
        raise NotImplementedError


class IncrementalController(ControllerWithArguments):
    def __call__(self, environ, start_response):
        req = get_req(environ)
        if self.arg_parsers != ([], {}):
            arg_parsers, kwarg_parsers = self.arg_parsers
            self.args = [a.parse(req) for a in arg_parsers]
            for k in kwarg_parsers:
                kwarg = kwarg_parsers[k].parse(req)
                if kwarg is not arguments.NoArgument:
                    self.kwargs[k] = kwarg
        try:
            resp_generator = self.func(req, *self.args, **self.kwargs)
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

    def url(self, *args, **kwargs):
        '''
        Finds first arg parser, asks it for the url it knows,
        and then passes this off to the app to do what it needs to do.
        '''
        arg_parsers, kwarg_parsers = self.arg_parsers
        parsers = list(arg_parsers)
        parsers.extend(kwarg_parsers.values())
        for parser in parsers:
            if isinstance(parser, arguments.UrlArgParser):
                url = parser.url(*args, **kwargs)
                return self.app.url(self, url)
        return self.app.url(self, '/')
        
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


def raw_controller(func):
    def replacement(environ, start_response):
        req = get_req(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement

def controller(func):
    def replacement(environ, start_response):
        req = get_req(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement
