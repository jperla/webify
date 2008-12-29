
def a(url, text, **kwargs):
    #TODO: jperla: use kwargs as arbitrary html attributes
    return '<a href="%(url)s">%(text)s</a>' % {'url':url, 'text':text}

