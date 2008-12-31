from __future__ import absolute_import

from . import apps
from . import controllers
from . import defaults
from . import http
from . import templates
from . import tests
from . import urls

def run(app):
    http.server.serve(app, host=defaults.host, port=defaults.port)


class App(object):
    def __init__(self, dispatcher=urls.dispatchers.SimpleDispatcher):
        self.dispatcher = dispatcher()
        self.app = None

    def controller(self, *args, **kwargs):
        register_url = self.dispatcher.urlize(*args, **kwargs)
        def decorator(c):
            if not isinstance(c, controllers.Controller):
                c = controllers.IncrementalController(c)
            c.app = self
            registered = register_url(c)
            return registered
        return decorator

    def simple_args(self, *args, **kwargs):
        def decorator(f):
            controller = controllers.IncrementalController(f)
            argumented = controllers.arguments.Arguments(*args, **kwargs)(controller)
            return argumented
        return decorator

    def subapp(self, *args, **kwargs):
        register_url = self.dispatcher.urlize(*args, **kwargs)
        def decorator(c):
            if not isinstance(c, controllers.Controller):
                c = controllers.IncrementalController(c)
            c.app = self
            registered = register_url(c)
            return registered
        return decorator

    def url(self, controller, controller_url):
        dispatcher_url = self.dispatcher.url(controller, controller_url)
        if self.app is None:
            return dispatcher_url
        else:
            return self.app.url(dispatcher_url)

    def __call__(self, environment, response):
        return self.dispatcher(environment, response)


