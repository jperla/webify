import http.status
import http.headers.content_type

status = http.status.ok
content_type = http.headers.content_type.html
headers = [content_type,]

status_and_headers = status, headers

host = '127.0.0.1'
port = '8080'
