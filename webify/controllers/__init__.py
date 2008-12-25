from __future__ import absolute_import
import types
import logging

from webob import Request, Response
from webob import exc

from .. import templates
from .. import defaults

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

def incremental_controller(func):
    logging.warning('incremental_controller deprecated, please use IncrementalController')
    def replacement(environ, start_response):
        req = get_req(environ)
        try:
            resp_generator = func(req)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = defaults.status_and_headers
            start_response(status, headers)
            return recursively_iterate(resp_generator)
    return replacement


class IncrementalController(object):
    def __init__(self, func):
        self.func = func
        self.args = list()

    def append_args(self, *args):
        self.args = args

    def __call__(self, environ, start_response):
        req = get_req(environ)
        try:
            resp_generator = self.func(req, *self.args)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = defaults.status_and_headers
            start_response(status, headers)
            return recursively_iterate(resp_generator)
    
def advanced_incremental_controller(func):
    logging.warning('advanced_incremental_controller deprecated, please use AdvancedIncrementalController')
    def replacement(environ, start_response):
        req = get_req(environ)
        try:
            resp_generator = func(req)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = resp_generator.next()
            start_response(status, headers)
            return recursively_iterate(resp_generator)
    return replacement

class AdvancedIncrementalController(object):
    def __init__(self, args=list()):
        self.args = args

    def __call__(self, func):
        def replacement(environ, start_response):
            req = get_req(environ)
            try:
                resp_generator = func(req, *self.args)
            except exc.HTTPException, e:
                resp = e
                return resp(environ, start_response)
            else:
                status, headers = resp_generator.next()
                start_response(status, headers)
                return recursively_iterate(resp_generator)
        return replacement

