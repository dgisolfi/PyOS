#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals

class Devices:
    """ The controller for all loaded devices """
    def __init__(self):
        _globals._hardware_clock_id = -1

    def hostClockPulse(self):
        # Increment the hardware (host) clock.
        _globals._os_clock += 1
        # Call the kernel clock pulse event handler.
        _globals._kernel.krnOnCPUClockPulse()
    
    """ Curses attributes to control host input """
    def hostEnableKeyboardInterrupt(self):
        _globals._console.screen.keypad(True)

    def hostDisableKeyboardInterrupt(self):
        _globals._console.screen.keypad(False)