#!/usr/bin/env python
import time

import webify

app = webify.defaults.app()

# Controllers
@app.controller(path='/')
def index(req):
    yield 'Hello, world!'

static_path = 'tests/apps/standard/static/'
static = app.subapp(path='/static')(webify.apps.standard.static(static_path))
    

# Middleware
from webify.middleware import install_middleware, EvalException
wrapped_app = install_middleware(app, [
                                       EvalException,
                                      ])

# Server
from webify.http import server
if __name__ == '__main__':
    server.serve(app, host='127.0.0.1', port='8080')

