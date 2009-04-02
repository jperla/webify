from __future__ import absolute_import

from ... import ArgParser, Controller, UrlArgParser

NoArgument = object()

class ArgParserWithDefault(ArgParser):
    def __init__(self, default):
        '''
        Init takes a default argument
        '''
        raise NotImplementedError


class Arguments(object):
    def __init__(self, *args):
        self.arg_parsers = args

    def __call__(self, controller):
        if not isinstance(controller, Controller):
            controller = Controller(c)
        controller.arg_parsers.extend(self.arg_parsers)
        return controller

class add(object):
    def __init__(self, arg_parser):
        self.arg_parser = arg_parser

    def __call__(self, f):
        controller = f if isinstance(f, Controller) else Controller(f)
        controller.arg_parsers.append(self.arg_parser)
        return controller

class RemainingUrl(UrlArgParser):
    def __init__(self, **kwargs):
        self.defaults = kwargs
        assert(len(self.defaults) <= 1)

    def parse(self, req):
        remaining = req.path_info[1:]
        args, kwargs = [], self.defaults
        if remaining != '':
            if len(self.defaults) == 1:
                kwargs[self.defaults.keys()[0]] = remaining
            else:
                args, kwargs = [remaining], {}
        return args, kwargs

    def url(self, remaining):
        return '/%s' % remaining

