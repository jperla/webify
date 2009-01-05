from __future__ import absolute_import

import os
import time
import signal

import webob
from webob import exc, Request, Response

def run(app, reload=False):
    http.server.serve(app, host=defaults.host, port=defaults.port)




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

class ArgParser(object):
    def __init__(self):
        raise NotImplementedError

    def parse(self, req):
        '''
        Returns arg or kwarg to append to controller call
        '''
        raise NotImplementedError

class UrlArgParser(ArgParser):
    def __init__(self):
        raise NotImplementedError

    def url(self, *args, **kwargs):
        raise NotImplementedError

class Template(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self.iterable

class CallableApp(object):
    def __init__(self, func):
        raise NotImplementedError

    def __call__(self, environ, start_response):
        raise NotImplementedError

class Controller(CallableApp):
    def __init__(self, func):
        assert(not isinstance(func, Controller))
        self.func = func
        self.arg_parsers = []
        self.superapp = None

    def url(self, *args, **kwargs):
        url_arg_parser = None
        for parser in self.arg_parsers:
            if isinstance(parser, UrlArgParser):
                url_arg_parser = parser
                break
        if url_arg_parser is None:
            suburl = '/'
        else:
            suburl = url_arg_parser.url(*args, **kwargs)
        if self.superapp is not None:
            return self.superapp.url(self, suburl)
        else:
            return suburl
    
    def __call__(self, environ, start_response):
        req = get_req(environ)
        args, kwargs = [], {}
        for parser in self.arg_parsers:
            parser_args, parser_kwargs = parser.parse(req)
            args.extend(parser_args)
            kwargs.update(parser_kwargs)
        resp_iterator = self.func(req, *args, **kwargs)

         #TODO: jperla: should also check to see if itself is superapp
        status, headers = http.defaults.status_and_headers
        first_yield = resp_iterator.next()
        if not isinstance(first_yield, exc.HTTPException):
            start_response(status, headers)
            return self.body([first_yield, resp_iterator])
        else:
            resp = exception = first_yield
            return resp(environ, start_response)

    def body(self, iterable):
        if self.superapp is not None:
            return self.superapp.body(recursively_iterate(iterable))
        else:
            return recursively_iterate(iterable)

from . import apps
from . import controllers
from . import defaults
from . import email
from . import http
from . import templates
from . import tests
from . import urls

