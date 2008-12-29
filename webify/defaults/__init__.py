from __future__ import absolute_import

from .. import urls as __urls
from .. import controllers as __controllers

from ..http.defaults import status, content_type, headers, status_and_headers

host = '127.0.0.1'
port = '8080'

dispatcher = __urls.dispatchers.SlashDispatcher
controller = __controllers.IncrementalController

mapper = __urls.mappers.SimpleMapper
