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


def recursively_iterate(item):
    if isinstance(item, str):
        raise Exception(u'Always work with unicode within your app!')
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
        self.response = []

    def __call__(self, x):
        self.print_response(x)

    def print_response(self, x):
        self.response.append(x)

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
            return output_encoding(recursively_iterate(p.response), 'utf8')

class App(object):
    def __init__(self):
        pass

    def __call__(self, req, p):
        raise NotImplementedError

def output_encoding(strings, encoding):
    for s in strings:
        if isinstance(s, unicode):
            print 'arst'
        else:
            print 'oien'
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
