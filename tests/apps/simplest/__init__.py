import webify

app = webify.App()

@app.controller()
@app.simple_args(name=webify.controllers.arguments.RemainingArgParser())
def hello(req, name='world'):
    times = req.params.get('times', '1')
    for i in xrange(int(times)):
        yield 'Hello, %s!<br />' % name

if __name__ == '__main__':
    webify.run(app)
    
# Try Loading http://127.0.0.1:8080/hello/world?times=1000000
