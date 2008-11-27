#!/usr/bin/env python
import time

import webify.defaults
from webify.controllers import controller, incremental_controller

@incremental_controller
def hello(req):
    assert(req.method == 'GET')
    yield webify.defaults.status_and_headers
    yield '''<form method="POST">'''
    yield '''Hello, world! <br />'''
    yield '''Your name: <input type="text" name="name">'''
    yield '''<input type="submit">'''
    yield '''</form>'''

from webify.urls.dispatchers import NoURLDispatcher
app = NoURLDispatcher(hello)

from webify.middleware import install_middleware, EvalException
wrapped_app = install_middleware(app, [
                                       EvalException,
                                      ])

from webify.http import server
if __name__ == '__main__':
    server.serve(app, host='127.0.0.1', port='8080')

