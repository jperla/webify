import re

def recursive_descent(template, position):
    pass

class ParseNode(object):
    def __init__(self, code, parent, indentation=0):
        self.code = code
        self.parent = parent
        self.children = []

    def child_generator(self):
        self.children = []
        next_child = []
        new_line = False
        for line in self.code:
            if line.startswith(' ' * self.indentation):
                line = line[self.indentation:]
            else:
                raise Exception('Indentation error for code: %s' % self.code)

            if line.startswith('yield'):
                next_child.append(line)
                new_line = True
            elif (line.startswith('if') or 
                  line.startswith('else') or 
                  line.startswith(' ')):
                next_child.append(line)

            if new_line:
                code = '\n'.join(next_child)
                if len(next_child) > 1:
                    re.match('( )*', next_child[1]).group(1)
                indentation = 
                self.children.append(ParsedNode(code, self, indentation))

            """
            if code.startswith('yield'):
                p = re.pattern(r"^if (.*) ", re.M | re.S)
                variable = re.match(, line).group(1)
                if variable in context:
                    indentation_stack.insert('if-true', 0)
            elif line.startswith('yield'):
                html = re.match(r"""yield '''(.*)'''$""", line).group(1)
                yield html
            """
        pass

    def __str__(self):
        return self.code

def set_indentations(template):
    return ParseNode(template, None)
    

def python_template(filename, context):
    template = open(filename, 'r').read()
    parsed = set_indentations(template)
    for line in parsed:
        yield line
