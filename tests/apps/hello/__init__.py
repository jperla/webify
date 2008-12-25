#!/usr/bin/env python
import time

import webify

# Controller
import webify.defaults
from webify.controllers import controller, advanced_incremental_controller

@advanced_incremental_controller
def hello(req):
    yield webify.defaults.status_and_headers
    yield '''<form method="POST">'''
    name = req.params.get('name', None)
    if name is None:
        yield '''Hello, world! <br />'''
    else:
        yield '''Hello, %(name)s! <br />''' % {'name': name}
    yield '''Your name: <input type="text" name="name">'''
    yield '''<input type="submit">'''
    yield '''</form>'''

# Urls
from webify.urls.dispatchers import NoURLDispatcher
app = NoURLDispatcher(hello)

# Middleware
from webify.middleware import install_middleware, EvalException
wrapped_app = install_middleware(app, [
                                       EvalException,
                                      ])

# Server
from webify.http import server
if __name__ == '__main__':
    server.serve(app, host='127.0.0.1', port='8080')

