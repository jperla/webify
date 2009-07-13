from contextlib import contextmanager

def h(text):
    #TODO: jperla: should sanitize html
    return text

def escape_javascript(js):
    return js

def a(url, text, **kwargs):
    options = u' '.join(u'%s="%s"' % (k, kwargs[k]) for k in kwargs)
    return u'<a href="%(url)s" %(options)s>%(text)s</a>' % {u'url':url, 
                                               u'text':h(text),
                                               u'options':options}

def h1(text):
    return u'<h1>%s</h1>\n' % h(text)

def h2(text):
    return u'<h2>%s</h2>\n' % h(text)

def h3(text):
    return u'<h3>%s</h3>\n' % h(text)

def br():
    return u'<br />\n'

def _generate_element(open, close):
    def new_element(html):
        return u'%s%s%s' % (open, html, close)
    return new_element

li = _generate_element(u'<li>', u'</li>\n')
p = _generate_element(u'<p>', u'</p>\n')
td = _generate_element(u'<td>', u'</td>')
b = _generate_element(u'<b>', u'</b>')
title = _generate_element(u'<title>', u'</title>')
span_smaller = _generate_element(u'<span style="font-size:smaller;">', u'</span>')

def _generate_container(open, end_open, close):
    #TODO: jperla: take default arguments
    @contextmanager
    def new_container(p, attrs={}):
        attribute_html = u' '.join(u'%s="%s"' % (a, attrs[a]) for a in attrs)
        p(open + attribute_html + end_open)
        yield p
        p(close)
    return new_container

def _generate_tag(tag_name):
    return _generate_container(u'<%s ' % tag_name, u'>', u'</%s>\n' % tag_name)

html = _generate_tag(u'html')
body = _generate_tag(u'body')
tr = _generate_tag(u'tr')
table = _generate_tag(u'table')
ol = _generate_tag(u'ol')
ul = _generate_tag(u'ul')
head = _generate_tag(u'head')
div = _generate_tag(u'div')
p_block = _generate_tag(u'p')
td_block = _generate_tag(u'td')
script_block = _generate_container(u'<script type="text/javascript"', u'><!--\n',
                             u'--></script>\n')

