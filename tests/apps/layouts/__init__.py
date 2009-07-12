#!/usr/bin/env python
import webify

# Layout app
layout = (u'''
<html><head>
<title>Hello App</title>
</head><body>
''', u'''
</body></html>
''')


app = webify.defaults.app()

@webify.single_app()
def layout_app(req, p, name):
    p(layout[0])
    app(req, p)
    p(layout[1])

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
wrapped_app = webify.wsgify(app, EvalException)


# Server
if __name__ == '__main__':
    webify.http.server.serve(wrapped_app, host='127.0.0.1', port='8080')

