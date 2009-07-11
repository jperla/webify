#<!-- coding=UTF-8 -->
from __future__ import absolute_import, with_statement
import re
import datetime

from .apps import first_template
from .apps import send_email
from .apps import hello
#from .apps import layouts
from .apps import simplest
from .apps import standard

import webify

from webify.tests import get, post, difference

def test_url():
    url = hello.hello.url()
    assert url == u'/hello/'
    
def test_index():
    with get(webify.wsgify(hello.app), '/') as r:
        assert u'200' in r.status
        assert u'Hello, world!' in r.body

def test_simplest():
    with get(webify.wsgify(simplest.app), '/world?times=3') as r:
        assert u'200' in r.status
        body = r.body
        assert u'world' in body
        assert u'Hello, world!' in body
        assert len(re.findall('world', body)) == 3

'''
def test_unicode():
    with get(webify.wsgify(simplest.app), '/wểrld?times=3') as r:
        assert u'200' in r.status
        assert u'wểrld' in r.body
        assert u'Hello, wểrld!' in r.body
        assert len(re.findall(u'wểrld', r.body)) == 3
'''

def test_simplest_hello():
    with get(webify.wsgify(simplest.app), '/') as r:
        assert u'200' in r.status
        assert u'world' in r.body
        assert u'Hello, world!' in r.body
        assert u'<br />' in r.body
        assert u'500' not in r.status
        assert u'Error' not in r.status
        assert u'Error' not in r.body

'''
def test_redirect():
    with get(webify.wsgify(hello.app), '/hello_old/') as r:
        assert u'302' in r.status
        assert u'/hello/' in r.body
'''


def test_remaining_url_arg_parser():
    with get(webify.wsgify(simplest.app), '/joe?times=10') as r:
        assert u'200' in r.status
        assert u'joe' in r.body
        assert u'Hello, joe!' in r.body
        assert len(re.findall(u'joe', r.body)) == 10
        assert u'Hello, joe!' in r.body

def test_time_diff():
    time = datetime.datetime.now()
    t = datetime.timedelta(days=3)
    diff = webify.templates.helpers.time.fuzzy_time_diff(time - t, time)
    assert u'days' in diff
    assert u'3' in diff
    assert u'4' not in diff
    assert u'hours' not in diff

def test_url_generation():
    hello = simplest.app.dispatcher.subapp
    url = hello.url('joe')
    assert url == u'/joe'

def test_template():
    with get(webify.wsgify(first_template.app), '/hello?name=joe') as r:
        assert u'200' in r.status
        assert u'joe' in r.body
        assert u'Hello, joe!' in r.body

'''
def test_layout():
    with get(webify.wsgify(layouts.app), '/hello?name=joe') as r:
        assert u'200' in r.status
        assert u'joe' in r.body
        assert u'Hello, joe!' in r.body
        assert u'<title>' in r.body
'''

def test_static_app():
    content = u'''div {\n    color: blue;\n}\n'''
    with get(webify.wsgify(standard.app), u'/static/style.css') as r:
        assert content == r.body

def test_send_email():
    with difference(lambda:len(send_email.mail_server.sent_email)):
        with get(send_email.wrapped_app, '/static/style.css') as r:
            assert u'200' in r.status
    

