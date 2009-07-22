from contextlib import contextmanager
import itertools


def h(text):
    #TODO: jperla: should sanitize html
    return u'%s' % text

def escape_javascript(js):
    return js

def a(url, text, attrs={}):
    options = u' '.join(u'%s="%s"' % (k, attrs[k]) for k in attrs)
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

def _generate_element(open, end_open, close, default_attrs):
    def new_element(html, attrs={}):
        attrs = __merge(default_attrs, attrs)
        attribute_html = u' '.join(u'%s="%s"' % (k, v) 
                                for k,v in attrs.iteritems() if v is not None)
        if attribute_html != u'':
            attribute_html = u' ' + attribute_html
        return open + attribute_html + end_open + html + close + u'\n'
    return new_element

def _generate_tag(name, attrs={}):
    return _generate_element(u'<%s' % name, u'>', u'</%s>' % name, attrs)

li = _generate_tag(u'li')
p = _generate_tag(u'p')
td = _generate_tag(u'td')
b = _generate_tag(u'b')
i = _generate_tag(u'i')
em = _generate_tag(u'em')
title = _generate_tag(u'title')
span = _generate_tag(u'span')
img = lambda src, attrs={}: _generate_tag(u'img')(u'', __merge({'src':src}, attrs))
span_smaller = _generate_tag(u'span', {u'style':'font-size:smaller;'})

script_src = lambda src: _generate_tag(u'script', 
                                       {u'type':u'text/javascript', 
                                        u'src':src})(u'')

link_css = lambda href,media=u'screen': _generate_tag(u'link', 
                                                      {u'type':u'text/css', 
                                                       u'rel':u'Stylesheet',
                                                       u'media':media,
                                                       u'href':href})(u'')

def _generate_container(open, end_open, close, default_attrs={}):
    #TODO: jperla: take default arguments
    def new_container(attrs={}):
        attrs = __merge(default_attrs, attrs)
        attribute_html = u' '.join(u'%s="%s"' % (k, v) 
                                for k,v in attrs.iteritems() if v is not None)
        if attribute_html != u'':
            attribute_html = u' ' + attribute_html
        return (open + attribute_html + end_open, close)
    return new_container

def _generate_block_tag(tag_name, default_attrs={}):
    return _generate_container(u'<%s' % tag_name, 
                               u'>', 
                               u'</%s>\n' % tag_name,
                               default_attrs)

html = _generate_block_tag(u'html')
body = _generate_block_tag(u'body')
tr = _generate_block_tag(u'tr')
table = _generate_block_tag(u'table')
ol = _generate_block_tag(u'ol')
ul = _generate_block_tag(u'ul')
head = _generate_block_tag(u'head')
div = _generate_block_tag(u'div')
button = _generate_block_tag(u'button')
p_block = _generate_block_tag(u'p')
li_block = _generate_block_tag(u'li')
td_block = _generate_block_tag(u'td')


def __merge(d1, d2):
    return dict([(k,v) for k,v in itertools.chain(d1.iteritems(), d2.iteritems())])

input = lambda attrs: _generate_tag(u'input',
                                    __merge({u'type':u'text'}, attrs))(u'')

def _generate_input(type):
    def new_input(name=None, value=None, id=None, attrs={}):
        return input(__merge({u'type':type,
                              u'name':name,
                              u'value':value,
                              u'id':id,}, attrs))
    return new_input

input_text = _generate_input(u'text')
input_submit = _generate_input(u'submit')
input_password = _generate_input(u'password')
input_hidden = _generate_input(u'hidden')
input_file = _generate_input(u'file')

def textarea(name=None, id=None, attrs={}):
    attrs = __merge({'name':name, 'id':id}, attrs)
    return _generate_block_tag(u'textarea', attrs)()

'''
form = _generate_block_tag(u'form', {u'method':u'POST', u'action':u''})
'''
def form(action=u'', method=u'POST', attrs={}):
    attrs = __merge({'action':action, 'method':method}, attrs)
    return _generate_block_tag(u'form', attrs)()

script_block = _generate_container(u'<script',
                                   u'><!--', 
                                   u'--></script>\n',
                                   {u'type':u'text/javascript'})

