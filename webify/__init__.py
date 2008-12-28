# Shortcuts for simplest
import defaults

from controllers import controller, IncrementalController
import urls

import http
def run(app):
    http.server.serve(app, host=defaults.host, port=defaults.port)

class Application(object):
    def __init__(self, 
                 dispatcher=defaults.dispatcher, 
                 controller=defaults.controller):
        urls = dispatcher(controller)
        self.urls = urls

    def controller(self, *args, **kwargs):
        return self.urls.wrap(*args, **kwargs)

    def __call__(self, environment, response):
        return self.urls(environment, response)
        
    
