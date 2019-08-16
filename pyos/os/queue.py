#!/usr/bin/env python3
# 2019-8-6

# A Python implementetation of a 
# Queue using an array
class Queue:
    def __init__(self):
        self._queue = []

    def __str__(self):
        return str(self._queue)
    
    def __repr__(self):
        return self._queue.__repr__()

    def __del__(self):
        self._queue = None

    @property
    def queue(self):
        return self._queue
    
    def enqueue(self, element):
        self._queue.append(element)

    def dequeue(self):
        element = self._queue[-1]
        del self._queue[-1]
        return element
    
    # Returns the object at the top of the Queue without removing it.
    def peek(self):
        return self._queue[-1]

    def length(self):
        return len(self._queue)

    