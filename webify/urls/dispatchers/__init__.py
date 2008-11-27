from webob import exc, Request, Response

def NoURLDispatcher(controller):
    def dispatcher(environ, start_response):
        req = Request(environ) 
        # ignore url; path info
        relative_url = req.path_info
        responds_to_url = True
        if responds_to_url:
            return controller(environ, start_response)
        else:
            return exc.HTTPNotFound()(environ, start_response)
    return dispatcher


