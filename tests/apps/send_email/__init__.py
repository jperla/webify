import webify

app = webify.apps.SingleApp()

@app.controller()
def send(req):
    email = req.params.get(u'email', u'nobody@jperla.com')
    mail_server = req.settings[u'mail_server']
    message = webify.email.create_text_message(u'nobody@jperla.com',
                                                [email],
                                                u'Hello, World!',
                                                u'I am sending you a text message')
    mail_server.send_message(message)
    yield u'Sent email.'

# Middleware
from webify.middleware import install_middleware, SettingsMiddleware

mail_server = webify.email.TestMailServer()
settings = {'mail_server': mail_server}
wrapped_app = install_middleware(app, [
                                       SettingsMiddleware(settings),
                                      ])


if __name__ == '__main__':
    webify.run(app)
    
# Try Loading http://127.0.0.1:8080/hello/world?times=1000000
