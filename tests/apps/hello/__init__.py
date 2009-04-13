#!/usr/bin/env python
import time

import webify

app = webify.defaults.app()

# Controllers
@app.controller(path='/')
def index(req):
    yield u'Hello, world!'

@app.controller()
def hello(req):
    yield u'<form method="POST">'
    name = req.params.get('name', None)
    if name is None:
        yield u'Hello, world! <br />'
    else:
        yield u'Hello, %(name)s! <br />' % {'name': name}
    yield u'Your name: <input type="text" name="name">'
    yield u'<input type="submit">'
    yield u'</form>'

@app.controller()
def hello_old(req):
    yield webify.http.status.redirect(hello.url())

# Middleware
from webify.middleware import install_middleware, EvalException
wrapped_app = install_middleware(app, [
                                       EvalException,
                                      ])

# Server
from webify.http import server
if __name__ == '__main__':
    server.serve(app, host='127.0.0.1', port=8080)

