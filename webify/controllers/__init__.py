from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from .. import http as _http

def get_req(environ):
    req = Request(environ)
    if 'settings' not in req.environ or req.environ['settings'] == []:
        req.settings = {} 
    else:
        req.settings = req.environ['settings'][0] 
    return req

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

def recursively_iterate(g):
    for item in g:
        if not hasattr(item, '__iter__'):
            yield item
        else:
            for subitem in recursively_iterate(item):
                yield subitem

class ControllerWithArguments(object):
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

NoArgument = object()

class ArgParser(object):
    def __init__(self):
        raise NotImplementedError

    def parse(self, req):
        '''
        Returns arg or kwarg to append to controller call
        '''
        raise NotImplementedError

class ArgParserWithDefault(ArgParser):
    def __init__(self, default):
        '''
        Init takes a default argument
        '''
        raise NotImplementedError



class UrlArgParser(ArgParser):
    def __init__(self):
        raise NotImplementedError

    def url(self, *args, **kwargs):
        raise NotImplementedError

class RemainingArgParser(UrlArgParser):
    def __init__(self):
        pass

    def parse(self, req):
        remaining = req.path_info[1:]
        if remaining != '':
            return remaining
        else:
            return NoArgument

    def url(self, remaining):
        return '/%s' % remaining

class Arguments():
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, controller):
        def add_args_to_controller(environ, start_response):
            controller.arg_parsers = (self.args, self.kwargs)
            return controller(environ, start_response)
        return add_args_to_controller

class IncrementalController(ControllerWithArguments):
    def __call__(self, environ, start_response):
        req = get_req(environ)
        if self.arg_parsers != ([], {}):
            self.args = [a.parse(req) for a in self.arg_parsers[0]]
            for k in self.arg_parsers[1]:
                kwarg = self.arg_parsers[1][k].parse(req)
                if kwarg is not NoArgument:
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
        for parser in self.arg_parsers:
            if isinstance(parser, UrlArgParser):
                url = parser.url(*args, **kwargs)
                return self.app.url(self, url)
        return self.app.url(self, '/')
        

class AdvancedIncrementalController(ControllerWithArguments):
    def __call__(self, environ, start_response):
        req = get_req(environ)
        try:
            resp_generator = self.func(req, *self.args, **self.kwargs)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            first_yield = resp_generator.next()
            if not isinstance(first_yield, exc.HTTPException):
                status, headers = first_yield
                start_response(status, headers)
                return recursively_iterate([first_yield, resp_generator])
            else:
                return first_yield(environ, start_response)

class UrlizedController(object):
    def __init__(self, controller, url_parser):
        self.controller = controller
        self.url_parser = url_parser
    
    def url(self, *args, **kwargs):
        return self.url_parser.url(*args, **kwargs)

    def __call__(self, environ, start_response):
        args, kwargs = self.url_parser.parse(environ)
        self.controller.append_args(args, kwargs)
        return self.controller(environ, start_response)

