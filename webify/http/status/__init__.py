from __future__ import absolute_import

import webob

ok = '200 OK'

def redirect(location, *args, **kwargs):
    redirect_status = webob.exc.HTTPFound
    return redirect_status(location=location)

def not_found(body=''):
    return webob.exc.HTTPNotFound()
