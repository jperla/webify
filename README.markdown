Webify
======
The lazy programmer's web framework.


Purpose
=======
You have an awesome offline program.  Webify and deploy it in under _5_ minutes.


Example: a complete Webify application
======================================

    import webify

    urls = webify.UrlWrapper()

    @urls.wrap(url_args=webify.UrlWrapper.Arguments.Path())
    def hello(req, name='world'):
        times = req.params.get('times', '1')
        for i in xrange(int(times)):
            yield 'Hello, %s!<br />' % name

    if __name__ == '__main__': 
        webify.run(urls.application())

Try and load http://127.0.0.1:8080/world?times=100000

Programming and Design Philosophy
=================================
* The Zen of Python
* Don't repeat yourself
* Simplicity over features
* Clarity over cleverness
* Explicit is better than implicit
* No magic
* Make only Order of Magnitude improvements
* Defaults over options
* Innovation over patterns
* Exactly one obvious way to do anything
* Build bottom-up as well as top-down
* Code less
* Don't repeat yourself
* Write sloppy, test quickly, rebuild cleanly
* No pagination

TODO
====
Webify includes 
- controllers
- templates, subtemplates, and layouts
- URL dispatching and redirects
- forms
- middleware
- a debugging and production server thread
- smallest python app period
- very extensible and easy to understand


Webify still needs, in order,
- Models and backend storage*
- Documentation, auto-generated from codebase, with auto-tests
- Sessions and authentication*
- Email
- Webapp testing framework with fixtures
- Pluggable sub-webapps*
- Auto-admin (databrowse?)*
- Standard template filters
- Synchronous and asynchronous signals and dispatchers*
- Cache system*
- Internationalization*
- CSRF protection
- Sitemaps
- RSS Feeds

*requires a hard design decision


Webify will never have
* { Braces }
* Pagination
* Clunky design
* Repetition
* Repetition


ACKNOWLEDGEMENTS
================
Webify borrows heavily from existing Python web architectures 
and thanks them profusely for their high quality.

Thank you WebOb and Paste for much of this code.  
Also, thank you Ian Bicking, Django developers, and Guido van Rossum 
for great design ideas and a high standard of excellence.

API
===
I strive for a bug-free master branch.  

As to the stability of the API and backwards-compatibility, 
I guarantee nothing.  In fact, I guarantee that I will change
the API many times, breaking unmodified applications, sometimes
purposefully to keep you mindful.

I will keep this promise both through the beta and after 1.0.

Legacy code kills the pace of development, snowballs cruft, 
and holds back the possibility of game-changing improvements.

On the other hand, branches of point versions may be maintained
with bug fixes for those who want to stay secure, but do not need
new features.


License
=======
MIT license

