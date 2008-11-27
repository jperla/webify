Webify
======
The lazy programmer's web framework.


Purpose
=======
You have an awesome offline program.  Webify and deploy it in under _5_ minutes.


Example: a complete Webify application
======================================
    import webify

    @webify.incremental_controller
    def hello(req):
        path = req.path_info[1:]
        name = path if path else 'world'
        times = int(req.params.get('times', 1))
        for i in xrange(times):
            yield 'Hello, %s!<br />' % name

    if __name__ == '__main__':
        webify.run(hello)
      
Try and load http://127.0.0.1:8080/world?times=100000


API
===
I strive for a bug-free master branch.  

As to the stability of the API and backwards-compatibility, 
I guarantee nothing.  In fact, I guarantee that I will change
the API many times, breaking unmodified applications, sometimes
purposefully to keep you mindful.

I will keep my promise both through the beta and after 1.0.

Legacy code kills the pace of development, snowballs cruft, 
and holds back the possibility of game-changing improvements.

On the other hand, branches of point versions may be maintained
with bug fixes for those who want to stay secure, but do not need
new features.


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

License
=======
MIT license
