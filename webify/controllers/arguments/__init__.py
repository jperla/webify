NoArgument = object()

class ArgParser(object):
    def __init__(self):
        raise NotImplementedError

    def parse(self, req):
        '''
        Returns arg or kwarg to append to controller call
        '''
        raise NotImplementedError

class ArgParserWithDefault(ArgParser):
    def __init__(self, default):
        '''
        Init takes a default argument
        '''
        raise NotImplementedError

class UrlArgParser(ArgParser):
    def __init__(self):
        raise NotImplementedError

    def url(self, *args, **kwargs):
        raise NotImplementedError

class RemainingArgParser(UrlArgParser):
    def __init__(self):
        pass

    def parse(self, req):
        remaining = req.path_info[1:]
        if remaining != '':
            return remaining
        else:
            return NoArgument

    def url(self, remaining):
        return '/%s' % remaining


class Arguments():
    def __init__(self, *args):
        self.arg_parsers = args

    def __call__(self, controller):
        controller.arg_parsers = self.arg_parsers
        return controller


class RemainingUrlArgParser(UrlArgParser):
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

