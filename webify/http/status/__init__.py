from __future__ import absolute_import

import webob

ok = '200 OK'

def redirect(location, *args, **kwargs):
    redirect_status = webob.exc.HTTPFound
    if isinstance(location, basestring):
        raise redirect_status(location=location)
    elif hasattr(location, 'url'):
        url = location.url(*args, **kwargs)
        raise redirect_status(location=url)
    else:
        raise Exception('Unkown redirect point')
