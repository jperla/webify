from contextlib import contextmanager

from webob import Request, Response
import types

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


@contextmanager
def difference(f, amount=None, message=''):
    assert(isinstance(f, types.FunctionType), 'difference() takes a function to call as the first argument which it calls twice: once before and once after')
    original = f()
    yield
    new = f()
    if amount == None:
        assert(original != new)
    else:
        assert(new - original == amount)


