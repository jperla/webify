from __future__ import absolute_import, with_statement
import re
import datetime

from webob import Request, Response

from .apps import simplest
from .apps import hello

import webify

from webify.tests import get, post

def test_url():
    url = hello.hello.url()
    assert url == '/hello/'
    

def test_simplest():
    with get(simplest.app, '/hello/world?times=3') as (status, body):
        assert '200' in status
        assert 'world' in body
        assert 'Hello, world!' in body
        assert len(re.findall('world', body)) == 3


def test_hello():
    with get(simplest.app, '/hello/') as (status, body):
        assert '200' in status
        assert 'world' in body
        assert 'Hello, world!' in body
        assert '<br />' in body
        assert '500' not in status
        assert 'Error' not in status
        assert 'Error' not in body

def test_redirect():
    with get(hello.app, '/hello_old/') as (status, body):
        assert '302' in status
        assert '/hello/' in body


def test_remaining_mapper():
    with get(simplest.app, '/hello/joe?times=10') as (status, body):
        assert '200' in status
        assert 'joe' in body
        assert 'Hello, joe!' in body
        assert len(re.findall('joe', body)) == 10
        assert 'Hello, joe!' in body

def test_time_diff():
    time = datetime.datetime.now()
    t = datetime.timedelta(days=3)
    diff = webify.templates.helpers.time.fuzzy_time_diff(time - t, time)
    assert 'days' in diff
    assert '3' in diff
    assert '4' not in diff
    assert 'hours' not in diff

