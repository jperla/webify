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
        if not isinstance(item, types.GeneratorType):
            yield item
        else:
            for subitem in recursively_iterate(item):
                yield subitem

class Controller(object):
    def __init__(self, func):
        self.func = func
        self.args = list()
        self.kwargs = {}

    def append_args(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, environ, start_response):
        pass

class IncrementalController(Controller):
    def __call__(self, environ, start_response):
        req = get_req(environ)
        try:
            resp_generator = self.func(req, *self.args, **self.kwargs)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = _http.defaults.status_and_headers
            start_response(status, headers)
            return recursively_iterate(resp_generator)
    

class AdvancedIncrementalController(Controller):
    def __call__(self, environ, start_response):
        req = get_req(environ)
        try:
            resp_generator = self.func(req, *self.args, **self.kwargs)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = resp_generator.next()
            start_response(status, headers)
            return recursively_iterate(resp_generator)

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

