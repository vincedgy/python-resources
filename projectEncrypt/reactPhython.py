"""
processDb : 
"""
from __future__ import print_function
from rx import  Observable, Observer

def testRx():
    #source = Observable.create(push_five_strings)
    #source.subscribe(PrintObserver())
    
    file = open('data.txt',mode='r')
    listValues = file.read().split();
    file.close()

    source2 = Observable.from_(listValues)
    source2.subscribe(on_next=lambda value: print("Received {0}".format(value)),
                      on_completed=lambda: print("Done!"),
                      on_error=lambda error: print("Error Occurred: {0}".format(error))
                     )
    source3 = Observable\
        .from_(listValues)\
        .map(lambda s: len(s))\
        .filter(lambda i: i >= 1)\
        .subscribe(lambda value: print("Received {0}".format(value)))

if __name__ == '__main__':
    testRx()