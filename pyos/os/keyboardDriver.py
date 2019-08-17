#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.os.deviceDriver import DeviceDriver
from pyos.globals import _globals

class KeyboardDriver(DeviceDriver):
    """ Handles all direct keyboard interactions """
    def __init__(self):
        # overide parent class attributes
        self.driver_entry = self.krnKbdDriverEntry
        self.isr = self.krnKbdDispatchKeyPress

    def krnKbdDriverEntry(self):
        # Initialization routine for this, 
        # the kernel-mode Keyboard Device Driver.
        self.status = 'loaded'
        # More?

    def krnKbdDispatchKeyPress(self, key_code):
        """Preforms logic on all incoming key presses for each key

        Attributes
        ----------
        key_code : int
            code of key pressed on keyboard
        """
        # The direct key code from the keyboard, shifted does not need to
        # be handled as curses handles this for us.

        
        if ((key_code >= 65 and key_code <= 90) # A..Z
            or (key_code >= 97 and key_code <= 123)): # a..z
            _globals._kernel.krnTrace(f'Key code: {key_code}')
            _globals._kernel_input_queue.enqueue(chr(key_code))

        # There is really no reason to seperate this into two if statements
        # other than style, there are a lot of cases to check, we cant send 
        # through all however as there are strange characters from scrolling 
        # and other actions that would throw us for a loop
        elif ((key_code >= 48 and key_code <= 57) # digits
            or key_code == 32                    # space
            or key_code == 3                     # ctrl + C
            or key_code == 13):                  # enter
                _globals._kernel.krnTrace(f'Key code: {key_code}')
                _globals._kernel_input_queue.enqueue(chr(key_code))
                