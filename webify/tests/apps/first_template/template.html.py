print('''<form method="POST">''')
if 'name' in context:
    print('''Hello, world! <br />''')
else:
    print('''Hello, %(name)s! <br />''' % context)
print('''Your name: <input type="text" name="name">''')
print('''<input type="submit">''')
print('''</form>''')
