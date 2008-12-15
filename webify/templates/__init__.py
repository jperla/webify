import subprocess
import re

def python_template(filename, context):
    template = open(filename, 'r').read()
    yield 'bla'
