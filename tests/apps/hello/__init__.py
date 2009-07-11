#!/usr/bin/env python
import time

import webify

app = webify.defaults.app()

# Controllers
@app.subapp(path='/')
@webify.urlable()
def index(req, p):
    p(u'Hello, world!')

@app.subapp()
@webify.urlable()
def hello(req, p):
    p(u'<form method="POST">')
    name = req.params.get('name', None)
    if name is None:
        p(u'Hello, world! <br />')
    else:
        p(u'Hello, %(name)s! <br />' % {'name': name})
    p(u'Your name: <input type="text" name="name">')
    p(u'<input type="submit">')
    p(u'</form>')

@app.subapp()
@webify.urlable()
def hello_old(req):
    yield webify.http.status.redirect(hello.url())

# Middleware
from webify.middleware import EvalException
wrapped_app = webify.wsgify(app, EvalException)

# Server
from webify.http import server
if __name__ == '__main__':
    server.serve(wrapped_app, host='127.0.0.1', port=8080)

