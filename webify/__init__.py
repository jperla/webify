# Shortcuts for simplest
import defaults

from controllers import controller, incremental_controller

import http
def run(app):
    http.server.serve(app, host=webify.defaults.host, port=webify.defaults.port)
