#!/usr/bin/env python
import time

import webify

app = webify.Application()

# Controllers
@app.simple_controller(path='')
def index(req):
    yield 'Hello, world!'

@app.controller()
def hello(req):
    yield '<form method="POST">'
    name = req.params.get('name', None)
    if name is None:
        yield 'Hello, world! <br />'
    else:
        yield 'Hello, %(name)s! <br />' % {'name': name}
    yield 'Your name: <input type="text" name="name">'
    yield '<input type="submit">'
    yield '</form>'

@app.controller()
def hello_old(req):
    raise webify.http.status.redirect(hello.url())

# Middleware
from webify.middleware import install_middleware, EvalException
wrapped_app = install_middleware(app, [
                                       EvalException,
                                      ])

# Server
from webify.http import server
if __name__ == '__main__':
    server.serve(app, host='127.0.0.1', port='8080')

