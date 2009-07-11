from __future__ import absolute_import

#import chardet

from ... import App

NoArgument = object()

class UrlableApp(App):
    def __call__(self, req, p):
        raise NotImplementedError
    def url(self, *args, **kwargs):
        raise NotImplementedError

def remaining_url(req):
    remaining = req.path_info[1:]
    # #TODO: jperla: add this later
    #chardet.decode
    remaining = remaining.decode(u'utf-8')
    return remaining
    
class RemainingUrlableApp(UrlableApp):
    def __init__(self, subapp):
        self.subapp = subapp

    def __call__(self, req, p):
        remaining = remaining_url(req)
        self.subapp(req, p, remaining)
        
    def url(self, remaining):
        return u'/%s' % remaining

class UrlableAppWrapper(object):
    def __init__(self, args_func=lambda req:[], url_func=lambda:u'/'):
        # Takes request object, returns tuple for args (or dict for kwargs??)
        self.args_func = args_func
        ##TODO: jperla:  Takes arbitrary, returns str or Url ?
        self.url_func = url_func

    def __call__(self, controller):
        url_func, args_func = self.url_func, self.args_func
        class UrlableAppDecorator(UrlableApp):
            def __init__(self, func):
                self.func = func
            def __call__(self, req, p):
                args = args_func(req)
                if isinstance(args, dict):
                    kwargs = args
                    args = []
                else:
                    kwargs = {}
                return self.func(req, p, *args, **kwargs)
            def url(self, *args, **kwargs):
                return url_func(*args, **kwargs)
        return UrlableAppDecorator(controller)



class RemainingUrlableAppWrapper(UrlableAppWrapper):
    def __init__(self,  
                 args_func=lambda req: (remaining_url(req),),
                 url_func=lambda remaining: u'/%s' % remaining):
        UrlableAppWrapper.__init__(self, args_func, url_func)

