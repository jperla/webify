from __future__ import absolute_import
import os

from ...controllers import webargs

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
            for line in open(path, 'rb').readlines():
                p(unicode(line))
        else:
            p(webify.http.status.not_found())
    return static



