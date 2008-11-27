import webify

@webify.incremental_controller
def hello(req):
    times = req.params.get('times', '1')
    name = req.path_info[1:] if req.path_info[1:] else 'world'
    for i in xrange(int(times)):
        yield 'Hello, %s!<br />' % name

if __name__ == '__main__': 
    webify.run(hello) # Load http://127.0.0.1:8080/world?times=1000000
