def outer_function():
    message = 'Hi'
    def inner_function():
        print '{}'.format(message)
    return inner_function()

outer_function()