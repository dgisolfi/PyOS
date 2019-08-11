from .deviceDriver import DeviceDriver
from pyos.globals import _globals

class KeyboardDriver(DeviceDriver):
    def __init__(self):
        self.driver_entry = self.krnKbdDriverEntry
        self.isr = self.krnKbdDispatchKeyPress

    def krnKbdDriverEntry(self):
        # Initialization routine for this, 
        # the kernel-mode Keyboard Device Driver.
        self.status = 'loaded'
        # More?

    def krnKbdDispatchKeyPress(self, key_code):
        # because key is passed in as a tuple it can be unpacked cleanly
        _globals._kernel.krnTrace(f'Key code: {key_code}')
        char = ''

        # check if the given character is valid...
       
        if (key_code >= 65 and key_code <= 90 or   # A..Z 
        key_code >= 97 and key_code <= 123):       # a..z
            # if is_shifted:
            char = chr(key_code)
            _globals._console.write(char)