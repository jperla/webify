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




Programming and Design Philosophy
=================================
* The Zen of Python
* Don't repeat yourself
* Simplicity over features
* Clarity over cleverness
* Explicit is better than implicit
* Make only Order of Magnitude improvements
* Defaults over options
* Exactly one obvious way to do anything
* Build bottom-up as well as top-down
* Don't repeat yourself
* Innovation over patterns
* NO MAGIC
* Write sloppy, test quickly, rebuild cleanly

License
=======
MIT license
