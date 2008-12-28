from __future__ import absolute_import
import wsgiref
import wsgiref.util

import webob

class Remaining(object):
    def __init__(self):
        pass

    def __call__(self, app, environ, start_response):
        path = environ['PATH_INFO']
        assert(path[0] == '/')
        remaining = path[1:]
        if remaining != '':
            app.append_args(remaining)
        return app(environ, start_response)

remaining = Remaining()

