
def h(text):
    return text

def a(url, text, **kwargs):
    #TODO: jperla: use kwargs as arbitrary html attributes
    return '<a href="%(url)s">%(text)s</a>' % {'url':url, 'text':h(text)}

def h1(text):
    return '<h1>%s</h1>' % h(text)

def h2(text):
    return '<h2>%s</h2>' % h(text)

def h3(text):
    return '<h3>%s</h3>' % h(text)
