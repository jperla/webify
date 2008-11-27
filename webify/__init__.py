# Shortcuts for simplest
import webify.defaults

import http
def run(app):
    http.server.serve(app, host=webify.defaults.host, port=webify.defaults.port)


from webify.controllers import controller, incremental_controller
