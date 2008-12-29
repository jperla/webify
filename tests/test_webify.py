from __future__ import absolute_import
import re
import datetime

from webob import Request, Response

from .apps import simplest
from .apps import hello

import webify

def test_url():
    url = hello.hello.url()
    assert url == '/hello/'
    

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

def test_redirect():
    hello_req = Request.blank('http://localhost/hello_old/')
    hello_resp = hello_req.get_response(hello.app)
    assert '302' in str(hello_resp)
    assert '/hello/' in str(hello_resp)


def test_remaining_mapper():
    req = Request.blank('http://localhost/hello/joe?times=3')
    resp = req.get_response(simplest.app)
    assert '200' in str(resp)
    assert 'joe' in str(resp)
    assert 'Hello, joe!' in str(resp)
    assert len(re.findall('joe', str(resp))) == 3
    assert 'Hello, joe!' in str(resp)

def test_time_diff():
    time = datetime.datetime.now()
    t = datetime.timedelta(days=3)
    diff = webify.templates.helpers.time.fuzzy_time_diff(time - t, time)
    assert 'days' in diff
    assert '3' in diff
    assert '4' not in diff
    assert 'hours' not in diff

