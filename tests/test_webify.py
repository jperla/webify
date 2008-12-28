from __future__ import absolute_import
import re

from webob import Request, Response

from .apps import simplest
from .apps import hello

def test_simplest():
    req = Request.blank('http://localhost/hello/world?times=3')
    resp = req.get_response(simplest.app)
    assert '200' in str(resp)
    assert 'world' in str(resp)
    assert 'Hello, world!' in str(resp)
    assert len(re.findall('world', str(resp))) == 3
    assert 'Hello, world!' in str(resp)

def test_hello():
    hello_req = Request.blank('http://localhost/hello/')
    hello_resp = hello_req.get_response(hello.app)
    assert '200' in str(hello_resp)
    assert 'world' in str(hello_resp)
    assert 'Hello, world!' in str(hello_resp)
    assert '<br />' in str(hello_resp)
    assert '500' not in str(hello_resp)
    assert 'Error' not in str(hello_resp)


