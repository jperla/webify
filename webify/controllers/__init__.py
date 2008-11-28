from __future__ import absolute_import

from webob import Request, Response
from webob import exc

from .. import defaults

def raw_controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
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
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement

def incremental_controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp_generator = func(req)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = defaults.status_and_headers
            start_response(status, headers)
            return resp_generator
    return replacement


    
def advanced_incremental_controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp_generator = func(req)
        except exc.HTTPException, e:
            resp = e
            return resp(environ, start_response)
        else:
            status, headers = resp_generator.next()
            start_response(status, headers)
            return resp_generator
    return replacement

