yield '''<form method="POST">'''
if name in context:
    yield '''Hello, world! <br />'''
else:
    yield '''Hello, %(name)s! <br />''' % context
yield '''Your name: <input type="text" name="name">'''
yield '''<input type="submit">'''
yield '''</form>'''
