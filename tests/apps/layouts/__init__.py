#!/usr/bin/env python
import webify

app = webify.defaults.app()

def Layout(object):
    def __init__(self, header, footer):
        self.header = header
        self.footer = footer

    def __call__(body_func):
        def body_decorator(template):
            yield self.header
            yield body_func(template)
            yield self.footer
        return body_decorator
    
layout = Layout('''
<html><head>
<title>Hello App</title>
</head><body>
''', '''
</body></html>
''')

app.body = layout(app.body)

# Controllers
@app.controller()
def hello(req):
    context = {'name': req.params.get('name', 'world')}
    yield hello_template(context, req)

# Templates
# This would normally be in a different file in a different module 
def hello_template(context, req):
    yield '''<form method="POST">'''
    yield '''Hello, %(name)s! <br />''' % context
    yield '''Your name: <input type="text" name="name">'''
    yield '''<input type="submit">'''
    yield '''</form>'''


# Middleware
from webify.middleware import install_middleware, EvalException
wrapped_app = install_middleware(app, [
                                       EvalException,
                                      ])

# Server
if __name__ == '__main__':
    webify.http.server.serve(app, host='127.0.0.1', port='8080')

