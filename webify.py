from webob import Request, Response
from webob import exc

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

