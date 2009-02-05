Webify
======
The lazy man's web framework.


Purpose
=======
You have an awesome offline program.  Webify and deploy it in under _5_ minutes.


Example: a complete Webify application
======================================

    import webify
    from webify.controllers import arguments

    app = webify.apps.SingleApp()

    @app.controller()
    @arguments.add(arguments.RemainingUrl())
    def hello(req, name='world'):
        times = req.params.get('times', '1')
        for i in xrange(int(times)):
            yield 'Hello, %s!<br />' % name

    if __name__ == '__main__':
        webify.run(app)

    # Try Loading http://127.0.0.1:8080/hello/world?times=1000000


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

- Controllers
- Templates and helpers
- Beautiful Urls
- Forms
- Middleware
- A production server thread
- Smallest python app period
- Very extensible and easy to understand
- Error handling framework
- Webapp testing framework
- Standard template filters
- Pluggable sub-webapps
- Natural code layout using modules
- Email framework


Webify still needs, in order,

- A debugging server thread
- Layout system for templates
- Documentation, auto-generated from codebase, with auto-tests
- Sessions and authentication*
- Models and backend storage*
- Testing framework fixtures
- Auto-admin (databrowse?)*
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

