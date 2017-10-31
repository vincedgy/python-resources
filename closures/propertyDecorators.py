# Decorators 
""" """
from __future__ import print_function
from functools import wraps
import time

class Employee:
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = self.first + '.' + self.last + '@email.com'
    
    def fullname(self)
        return '{} {}'.format(self.first, self.last)

   
emp_1 = Employee('John', 'Smith')

print(emp_1.first)
print(emp_1.last)
print(emp_1.fullname())
