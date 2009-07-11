#!/usr/bin/env python
import webify

app = webify.defaults.app()


# Controllers
@app.subapp()
@webify.urlable()
def hello(req, p):
    context = {u'name': req.params.get(u'name', u'world')}
    p(hello_template(context, req))

# Templates
# This would normally be in a different file in a different module 
def hello_template(context, req):
    yield u'form method="POST">'
    yield u'Hello, %(name)s! <br />' % context
    yield u'Your name: <input type="text" name="name">'
    yield u'input type="submit">'
    yield u'form>'


# Middleware
from webify.middleware import EvalException
wsgi_app = webify.wsgify(app, EvalException)

# Server
if __name__ == '__main__':
    webify.http.server.serve(wsgi_app, host='127.0.0.1', port='8080')

