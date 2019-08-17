#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class Queue:
    """ A Python implementetation of a Queue using an array """
    def __init__(self):
        self._queue = []

    def __str__(self):
        """Represents the queue in string form

        This is done using calling list class' __str__ method
        """
        return str(self._queue)
    
    def __repr__(self):
        return self._queue.__repr__()

    def __del__(self):
        self._queue = None

    @property
    def queue(self):
        """ Define the array as a property """
        return self._queue
    
    def enqueue(self, element):
        """ place the element at 'the back of the line' """
        self._queue.append(element)

    def dequeue(self):
        """ Move the element from first in 'line' to off the 'line' """
        return self._queue.pop(0)
    
    def peek(self):
        """ Returns the object at the top of the Queue without removing it. """
        return self._queue[-1]

    def length(self):
        """ How many elements are in the Queue (list) """
        return len(self._queue)

    