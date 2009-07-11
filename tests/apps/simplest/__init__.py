import webify

@webify.single_app()
def app(req, p, name):
    times = req.params.get(u'times', 1)
    for i in xrange(int(times)):
        p(u'Hello, %s!<br />' % (name or u'world'))

if __name__ == '__main__':
    webify.run(webify.wsgify(app))
    
# Try Loading http://127.0.0.1:8080/hello/world?times=1000000
