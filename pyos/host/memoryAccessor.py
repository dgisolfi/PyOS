#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals

@_globals._utils.singleton
class MemoryAccessor:
    """ Manages all segments of memory and enforces boundaries """
    def read(self, address):
        pass

    def readBlock(self):
        pass

    def write(self, address, data):
        pass

    def checkBounds(self):
        pass
    