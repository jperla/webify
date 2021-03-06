from __future__ import absolute_import

from .. import urls as __urls
from .. import controllers as __controllers
from .. import apps as __apps

from ..http.defaults import status, content_type, headers, status_and_headers
from ..urls.defaults import dispatcher

host = u'127.0.0.1'
port = 8080

app = __apps.DispatcherApp
