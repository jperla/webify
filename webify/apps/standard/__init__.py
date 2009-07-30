from __future__ import absolute_import
import os

import chardet
import codecs

from ...controllers import webargs
from ...http.headers import content_types

def static(file_root='static/'):
    '''
    static = app.subapp(path='/static')(webify.apps.standard.static(file_root='static/'))
    '''
    @webargs.RemainingUrlableAppWrapper()
    #TODO: jperla: assert that p must be a OverridablePage
    def static(req, p, filename):
        #TODO: jperla: cache the static stuff forever
        # #TODO: jperla: Note: security problem
        path = os.path.join(file_root, filename)
        if os.path.exists(path) and os.path.isfile(path):
            #TODO: jperla: make this read in chunks
            encoding = 'raw_unicode_escape'#chardet.detect(path)['encoding']
            #TODO: jperla: switch on image type
            p.headers = [content_types.image_png]
            #p(codecs.open(path, 'rb', encoding).read())
            p(open(path, 'rb').read())
        else:
            #TODO: jperla: webify is not defined; namespace it
            p(webify.http.status.not_found())
    return static



