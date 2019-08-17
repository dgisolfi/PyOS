#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class Interrupt:
    """ Holds request number and all relavant params to that request """
    def __init__(self, irq, params):
        self.irq = irq
        self.params = params