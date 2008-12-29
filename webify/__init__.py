from __future__ import absolute_import

from . import defaults

from . import controllers
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
            if not isinstance(c, controllers.Controller):
                c = controllers.IncrementalController(c)
            c.app = self
            return urlized(c)
        return decorator

    def simple_args(self, *args, **kwargs):
        def decorator(f):
            controller = controllers.IncrementalController(f)
            argumented = controllers.arguments.Arguments(*args,
                                                         **kwargs)(controller)
            return argumented
        return decorator

    def url(self, controller, controller_url):
        return self.dispatcher.url(controller, controller_url)

    def __call__(self, environment, response):
        return self.dispatcher(environment, response)


