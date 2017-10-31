# Decorators 
""" """

def outer_function(msg):
    message = 'Hi'
    def inner_function():
        print '{}'.format(msg)
    return inner_function

hi_func = outer_function('Hi')
hello_func = outer_function('Hello')

hi_func()
hello_func()

