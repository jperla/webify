from __future__ import absolute_import

from . import charsets as __charsets

def content_type(type):
    return ('Content-Type', type)

html = content_type('text/html')
plain = content_type('text/plain')

html_utf8 = content_type('text/html; %s' % __charsets.utf8)
