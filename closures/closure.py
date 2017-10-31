# Decorators 
""" """
from __future__ import print_function

def decorator_function(original_function):
    def wrapper_function():
        return original_function()
    return wrapper_function

def display():
    print('display function ran')

decorator_display = decorator_function(display)

decorator_display()
