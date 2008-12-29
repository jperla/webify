from __future__ import absolute_import

from ...controllers import UrlizedController

class Mapper(object):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def map(self, f, controller):
        raise NotImplementedError

class RegexMapper(Mapper):
    def regex(self, f):
        raise NotImplementedError

class HashMapper(Mapper):
    def key(self, f):
        raise NotImplementedError

    def key_for_path(self, path):
        raise NotImplementedError

class PathMapper(Mapper):
    def path(self, f):
        raise NotImplementedError

class SimpleMapper(HashMapper, PathMapper):
    def __init__(self, path=None):
        self.__path = path

    def path(self, f):
        return '/%s/' % f.func_name if self.__path is None else self.__path

    def map(self, f, controller):
        p = SimpleParser(self.path(f))
        c = controller(f)
        urlized = UrlizedController(c, p)
        return urlized 

    def key(self, f):
        return self.path(f).strip('/')

    def key_for_path(self, path):
        name = environ['PATH_INFO'].split('/')[1]
        return name
        
class RemainingMapper(HashMapper, PathMapper):
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
        return self.path(f).strip('/')

    def key_for_path(self, path):
        name = environ['PATH_INFO'].split('/')[1]
        return name




class SimpleParser(object):
    def __init__(self, path='/'):
        self.path = path

    def url(self):
        return self.path
        
    def parse(self, environ):
        path = environ['PATH_INFO']
        assert(path.startswith(self.path))
        args, kwargs = [], {}
        return (args, kwargs)
        
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
            args = (remaining,)
        else:
            args = []
        kwargs = {}
        return (args, kwargs)

