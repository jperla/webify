#!/usr/bin/env python
import time

import webify

# Controller
import webify.defaults
from webify.controllers import (controller,
                               advanced_incremental_controller,
                               python_template_controller)

@python_template_controller
def hello(req):
    filename = '/home/jperla/projects/webify/webify/tests/apps/first_template/template.html.py'
    context = {}
    name = req.params.get('name', None)
    if name is not None:
        context['name'] = name
    return filename, context

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

