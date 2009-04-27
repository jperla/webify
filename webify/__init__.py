from __future__ import absolute_import

import os
import time
import types

def run(app, reload=False):
    http.server.serve(app, host=defaults.host, port=defaults.port, reload=reload)


def get_req(environ):
    req = http.Request(environ)
    if u'settings' not in req.environ or req.environ[u'settings'] == []:
        req.settings = {} 
    else:
        req.settings = req.environ[u'settings'][0] 
    return req


def recursively_iterate(g):
    for item in g:
        if isinstance(item, str):
            raise Exception(u'Always work with unicode within your app!')
        elif isinstance(item, unicode):
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
            suburl = u'/'
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

        # TODO: jperla: should also check to see if itself is superapp
        first_yield = resp_iterator.next()
        #TODO: jperla: confusing logic
        if not isinstance(first_yield, http.status.HTTPController):
            if isinstance(first_yield, types.TupleType):
                #TODO: jperla: do more explicit type checking
                if len(first_yield) != 2:
                    raise Exception(u'Too many items in states/headers tuple: %s' % first_yield)
                status, headers = first_yield
                start_response(status, headers)
                return self.body(resp_iterator)
            else:
                status, headers = http.defaults.status_and_headers
                start_response(status, headers)
                return self.body([first_yield, resp_iterator])
        else:
            resp = exception = first_yield
            return resp(environ, start_response)

    def body(self, iterable):
        if self.superapp is not None:
            return output_encoding(self.superapp.body(recursively_iterate(iterable)), u'utf-8')
        else:
            #TODO: jperla: detect encoding; don't just use utf-8
            return output_encoding(recursively_iterate(iterable), u'utf-8')

def output_encoding(strings, encoding):
    for s in strings:
        encoded = s.encode(encoding)
        yield encoded

from . import apps
from . import controllers
from . import defaults
from . import email
from . import http
from . import templates
from . import tests
from . import urls

