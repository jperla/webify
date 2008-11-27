from paste.evalexception import EvalException

def install_middleware(app, middleware):
    for m in middleware:
        app = m(app)
    return app

