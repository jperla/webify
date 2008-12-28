from __future__ import absolute_import

from ..urls import dispatchers as __dispatchers
from .. import controllers as __controllers

from ..http.defaults import status, content_type, headers, status_and_headers

host = '127.0.0.1'
port = '8080'

dispatcher = __dispatchers.Shifter
controller = __controllers.IncrementalController

