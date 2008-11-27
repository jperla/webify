import re

from webob import Request, Response

import apps.simplest
import apps.hello

def test_simplest():
    req = Request.blank('http://localhost/world?times=3')
    resp = req.get_response(apps.simplest.hello)
    assert '200' in str(resp)
    assert 'world' in str(resp)
    assert 'Hello, world!' in str(resp)
    assert len(re.findall('world', str(resp))) == 3
    assert 'Hello, world!' in str(resp)

def test_hello():
    hello_req = Request.blank('http://localhost/hello')
    hello_resp = hello_req.get_response(apps.hello.app)
    assert '200' in str(hello_resp)
    assert 'world' in str(hello_resp)
    assert 'Hello, world!' in str(hello_resp)
    assert '<br />' in str(hello_resp)
    assert '500' not in str(hello_resp)
    assert 'Error' not in str(hello_resp)


