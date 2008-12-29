from __future__ import absolute_import

from . import time

def pluralize(variable, plural='s', zero='s', word=''):
    length = len(variable)
    if length == 1:
        return word
    elif length == 0:
        return word + zero
    else:
        return word + plural
