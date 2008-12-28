class UrlizedController(object):
    def __init__(self, controller, url_parser):
        self.controller = controller
        self.url_parser = url_parser
    
    def url(self, *args, **kwargs):
        return self.url_parser.url(*args, **kwargs)

    def __call__(self, environ, start_response):
        args, kwargs = self.url_parser.parse(environ)
        self.controller.append_args(args, kwargs)
        return self.controller(environ, start_response)
        
class RemainingParser(object):
    def __init__(self, prefix='/'):
        self.prefix = prefix

    def url(self, remaining):
        return self.prefix + remaining

    def parse(self, environ):
        path = environ['PATH_INFO']
        assert(path.startswith(self.prefix))
        remaining = path[len(self.prefix):]
        if remaining != '':
            args = [remaining]
        else:
            args = []
        kwargs = {}
        return (args, kwargs)

class RemainingMapper(object):
    def __init__(self, path=None):
        self.__path = path

    def path(self, f):
        return '/%s/' % f.func_name if self.__path is None else self.__path

    def map(self, f, controller):
        p = RemainingParser(self.path(f))
        c = controller(f)
        urlized = UrlizedController(c, p)
        return urlized 

    def key(self, f):
        #TODO: jperla: not quite right
        return self.path(f).replace('/', '')

