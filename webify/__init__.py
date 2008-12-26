# Shortcuts for simplest
import defaults

from controllers import controller, IncrementalController
from urls import UrlWrapper

import http
def run(app):
    http.server.serve(app, host=webify.defaults.host, port=webify.defaults.port)
