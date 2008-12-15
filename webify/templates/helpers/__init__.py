def pluralize(variable, plural='s', zero='s', word=''):
    length = len(variable)
    if length == 1:
        return word
    elif length == 0:
        return word + zero
    else:
        return word + plural
