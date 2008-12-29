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
                 dispatcher=urls.dispatchers.SlashDispatcher,
                 default_controller=defaults.controller,
                 default_mapper=defaults.mapper):
        self.dispatcher = dispatcher(default_controller,
                                     default_mapper())

    def simple_controller(self, path=None, mapper=None, controller=None):
        if controller is None:
            controller = defaults.controller
        if mapper is None:
            mapper = defaults.mapper
        if path is not None:
            assert(isinstance(mapper, urls.mappers.PathMapper),
                    'This mapper does not support path name changes')
        return self.dispatcher.urlize(mapper=mapper(path))

    def controller(self, *args, **kwargs):
        return self.dispatcher.urlize(*args, **kwargs)

    def __call__(self, environment, response):
        return self.dispatcher(environment, response)
        

