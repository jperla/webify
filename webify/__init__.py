from __future__ import absolute_import

from . import defaults

from .controllers import controller, IncrementalController
from . import urls
from . import http
from . import templates
from . import tests

def run(app):
    http.server.serve(app, host=defaults.host, port=defaults.port)


class App(object):
    def __init__(self, dispatcher=urls.dispatchers.SimpleDispatcher):
        self.dispatcher = dispatcher()

    def controller(self, *args, **kwargs):
        urlized = self.dispatcher.urlize(*args, **kwargs)
        def decorator(c):
            c.app = self
            return urlized(c)
        return decorator

    def url(self, controller, controller_url):
        return self.dispatcher.url(controller, controller_url)

    def __call__(self, environment, response):
        return self.dispatcher(environment, response)


