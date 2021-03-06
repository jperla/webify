from __future__ import absolute_import
from contextlib import contextmanager

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


def recursively_iterate(item):
    if isinstance(item, str):
        raise Exception(u'Always work with unicode within your app: %s', item)
    elif isinstance(item, unicode):
        yield item
    else:
        for subitem in item:
            for i in recursively_iterate(subitem):
                yield i

def Url(object):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

class Page(object):
    def __init__(self, start_response):
        self.start_response = start_response
        status, headers = http.defaults.status_and_headers
        self.status = status
        self.headers = headers
        self.__response = []

    def __call__(self, x):
        self.print_response(x)

    def response(self):
        #TODO: jperla: serious work needed here
        if self.headers[0] == http.headers.content_types.html_utf8:
            return output_encoding(recursively_iterate(self.__response), 'utf8')
        else:
            return self.__response

    def print_response(self, x):
        self.__response.append(x)

class WSGIApp(object):
    def __init__(self, app):
        assert(isinstance(app, App))
        self.app = app

    def __call__(self, environ, start_response):
        req = get_req(environ)
        p = Page(start_response)
        try:
            self.app(req, p)
        except http.status.HTTPController, exception:
            resp = exception
            return resp(environ, start_response)
        else:
            start_response(p.status, p.headers)
            return p.response()

class App(object):
    def __init__(self):
        self.parent = None

    def __call__(self, req, p):
        raise NotImplementedError
    
    def wrap_parent(f):
    #TODO: jperla: use this everywhere somehow
        def decorator(self, subapp, suburl):
            if self.parent is None:
                return suburl
            else:
                return self.parent.wrap_url(self, suburl)
        return decorator
            
    @wrap_parent
    def wrap_url(self, subapp, suburl):
        return suburl

def output_encoding(strings, encoding):
    for s in strings:
        encoded = s.encode(encoding)
        yield encoded

from . import apps
from . import controllers
from . import defaults
from . import email
from . import http
from . import middleware
from . import templates
from . import tests
from . import tools
from . import urls

urlable = controllers.webargs.UrlableAppWrapper

def wsgify(app, *middleware_to_apply):
    return middleware.install_middleware(WSGIApp(app), middleware_to_apply)

#TODO: jperla: add prefix here
def single_app():
    def decorator(f):
        app = apps.SingleApp()
        app.subapp()(controllers.webargs.RemainingUrlableAppWrapper()(f))
        return app
    return decorator

def template():
    def decorator(f):
        class Catcher(object):
            def __init__(self):
                self.caught = []
            def __call__(self, r):
                if isinstance(r, unicode):
                    self.caught.append(r)
                elif isinstance(r, tuple) and len(r) == 2:
                    start,end = r
                    assert(isinstance(start, unicode))
                    assert(isinstance(end, unicode))
                    class X(object):
                        def __init__(self, c):
                            self.c = c
                        def __enter__(self):
                            self.c.append(start)
                        def __exit__(self, type, value, tb):
                            #TODO: jperla: figure out how to deal with this
                            self.c.append(end)
                    return X(self.caught)
                elif isinstance(r, str):
                    #TODO: jperla: unify this
                    raise Exception('unicode: %s' % r)
                else:
                    raise Exception('Unknown parameter, try sub()')
            def sub(self, t):
                self.caught.append(t)
        def new_f(*args, **kwargs):
            catcher = Catcher()
            f(catcher, *args, **kwargs)
            return ''.join(catcher.caught)
        return new_f
    return decorator

