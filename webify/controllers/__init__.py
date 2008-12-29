from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from . import arguments
from .. import http as _http

class Controller(object):
    def __init__(self, func):
        raise NotImplementedError

    def __call__(self, environ, start_response):
        raise NotImplementedError

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
