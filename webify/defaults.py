import http.status
import http.headers.content_type

status = http.status.ok
content_type = http.headers.content_type.html
headers = [content_type,]

status_and_headers = status, headers
