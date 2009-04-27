from __future__ import absolute_import

#import chardet

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
        # jperla: add this later
        #chardet.decode
        remaining = remaining.decode(u'utf-8')
        
        args, kwargs = [], self.defaults
        if remaining != u'':
            if len(self.defaults) == 1:
                kwargs[self.defaults.keys()[0]] = remaining
            else:
                args, kwargs = [remaining], {}
        return args, kwargs

    def url(self, remaining):
        return u'/%s' % remaining

class SettingsArgParser(UrlArgParser):
    #TODO: jperla: make this more powerful
    def __init__(self, setting_name, default=None):
        self.setting_name = setting_name
        self.default = default

    def parse(self, req):
        args, kwargs = [], {}
        kwargs[self.setting_name] = req.settings[self.setting_name]
        return args, kwargs

    def url(self, remaining):
        return '/%s' % remaining
