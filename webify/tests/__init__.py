from contextlib import contextmanager

from webob import Request, Response

@contextmanager
def get(app, url, host='http://localhost'):
    req = Request.blank(host + url)
    resp = req.get_response(app)
    yield str(resp.status), str(resp.body)

@contextmanager
def post(app, url, data, host='http://localhost'):
    req = Request.blank(host + url)
    req.method = 'POST'
    for key in data:
        req.POST[key] = data[key]
    resp = req.get_response(app)
    yield str(resp.status), str(resp.body)


