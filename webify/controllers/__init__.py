from __future__ import absolute_import

import types
import logging

from .. import http

def raw_controller(func):
    def replacement(environ, start_response):
        req = get_req(environ)
        try:
            resp = func(req, **req.urlvars)
        except http.status.HTTPController, e:
            resp = e
        if isinstance(resp, basestring):
            resp = http.Response(body=resp)
        return resp(environ, start_response)
    return replacement

def controller(func):
    def replacement(environ, start_response):
        req = get_req(environ)
        try:
            resp = func(req, **req.urlvars)
        except http.status.HTTPController, e:
            resp = e
        if isinstance(resp, basestring):
            resp = http.Response(body=resp)
        return resp(environ, start_response)
    return replacement
