from webob import Request, Response

import app.manage

def test_hello():
    hello_req = Request.blank('http://localhost/hello')
    hello_resp = hello_req.get_response(app.manage.app)
    assert 'Hello, world!' in str(hello_resp)
    assert '<br />' in str(hello_resp)
    assert '200' in str(hello_resp)
    assert '500' not in str(hello_resp)
    assert 'Error' not in str(hello_resp)


