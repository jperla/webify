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
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, controller):
        controller.arg_parsers = (self.args, self.kwargs)
        return controller

