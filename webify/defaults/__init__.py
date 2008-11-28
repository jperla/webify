from __future__ import absolute_import

from ..http import status as __status
from ..http.headers import content_type as __content_type

status = __status.ok
content_type = __content_type.html
headers = [content_type,]

status_and_headers = status, headers

host = '127.0.0.1'
port = '8080'
