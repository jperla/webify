from __future__ import absolute_import
import os

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
            for line in open(path, 'rb').readlines():
                yield unicode(line)
        else:
            yield webify.http.status.not_found()
    return static



