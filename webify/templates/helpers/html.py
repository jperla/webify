
def h(text):
    return text

def escape_javascript(js):
    return js

def a(url, text, **kwargs):
    options = ' '.join('%s="%s"' % (k, kwargs[k]) for k in kwargs)
    return '<a href="%(url)s" %(options)s>%(text)s</a>' % {'url':url, 
                                               'text':h(text),
                                               'options':options}

def h1(text):
    return '<h1>%s</h1>' % h(text)

def h2(text):
    return '<h2>%s</h2>' % h(text)

def h3(text):
    return '<h3>%s</h3>' % h(text)
