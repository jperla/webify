from __future__ import absolute_import
import os

import codecs

from ...controllers import webargs

class PrefixApp(webify.apps.App):
    def __init__(self, subapp, prefix):
        self.prefix = prefix
        self.subapp = subapp

    def __call__(self, req, p):
        assert(req.environ[u'PATH_INFO'].startswith(self.prefix))
        req.environ[u'PATH_INFO'] = req.environ[u'PATH_INFO'][len(self.prefix):]
        self.subapp(req, p)

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
            p(codecs.open(path, 'rb', 'utf-8').read())
        else:
            p(webify.http.status.not_found())
    return static



