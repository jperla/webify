import webify

urls = webify.UrlWrapper()

@urls.wrap(url_args=webify.UrlWrapper.Arguments.Path())
def hello(req, name='world'):
    times = req.params.get('times', '1')
    for i in xrange(int(times)):
        yield 'Hello, %s!<br />' % name

if __name__ == '__main__': 
    webify.run(urls.application()) # Load http://127.0.0.1:8080/world?times=1000000
