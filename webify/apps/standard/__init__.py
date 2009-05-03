from __future__ import absolute_import
import os

import codecs

from ...controllers import webargs

def static(file_root='static/'):
    '''
    static = app.subapp(path='/static')(webify.apps.standard.static(file_root='static/'))
    '''
    @webargs.add(webargs.RemainingUrl())
    def static(req, filename):
        #TODO: jperla: cache the static stuff forever
        # #TODO: jperla: Note: security problem
        path = os.path.join(file_root, filename)
        if os.path.exists(path) and os.path.isfile(path):
            #TODO: jperla: make this read in chunks
            yield codecs.open(path, 'rb', 'utf-8').read()
        else:
            yield webify.http.status.not_found()
    return static



