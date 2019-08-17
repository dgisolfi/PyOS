#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class DeviceDriver:
    """ Base Class for Drivers """
    def __init__(self):
        self.version = '0.07'
        self.status = 'unloaded'
        self.preemptable = False
        self.driver_entry = None
        self.isr = None