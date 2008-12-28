from __future__ import absolute_import
# Shortcuts for simplest
from . import defaults

from .controllers import controller, IncrementalController
from . import urls
from . import http

def run(app):
    http.server.serve(app, host=defaults.host, port=defaults.port)

class Application(object):
    def __init__(self,
                 dispatcher=urls.parsers.SlashDispatcher,
                 default_controller=defaults.controller):
        self.dispatcher = dispatcher(default_controller)

    def controller(self, *args, **kwargs):
        return self.dispatcher.urlize(*args, **kwargs)

    def __call__(self, environment, response):
        return self.dispatcher(environment, response)
        

