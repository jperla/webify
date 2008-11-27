from webob import Request, Response
from webob import exc

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
            status, headers = resp_generator.next()
            start_response(status, headers)
            return resp_generator
    return replacement


    
