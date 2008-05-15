from webify import controller

@controller
def index(req):
    if req.method == 'POST':
        return 'Hello %s!' % req.POST.get('name', 'No Name')
    elif req.method == 'GET':
        return '''<form method="POST">
                  You're name: <input type="text" name="name">
                  <input type="submit">
                  </form>'''

