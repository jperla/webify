
def h(text):
    return text

def escape_javascript(js):
    return js

def a(url, text, **kwargs):
    options = u' '.join(u'%s="%s"' % (k, kwargs[k]) for k in kwargs)
    return u'<a href="%(url)s" %(options)s>%(text)s</a>' % {u'url':url, 
                                               u'text':h(text),
                                               u'options':options}

def h1(text):
    return u'<h1>%s</h1>' % h(text)

def h2(text):
    return u'<h2>%s</h2>' % h(text)

def h3(text):
    return u'<h3>%s</h3>' % h(text)
