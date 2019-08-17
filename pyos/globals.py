#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.utils import Utils

class Globals:
    def __init__(self):
        """ global constants """
        self._APP_NAME = 'PyOS'
        self._APP_VERSION = '0.1'
        # 100 ms
        self._CPU_CLOCK_INTERVAL = 0.01
        self.TIMER_IRQ = 0
        self.KEYBOARD_IRQ = 1

        """ global variables """
        self._cpu = object
        self._os_clock = 0
        # (currently unused)  0 = Kernel Mode, 1 = User Mode
        self._mode = 0

        self._trace = True

        # Os Kernal
        self._kernel = object
        self._kernel_interrupt_queue = object
        self._kernel_input_queue = object
        self._kernel_buffers = []
        
        self._console = object
        self._shell = object

        self._devices = object

        self._sarcastic_mode = False

        self._krn_keyboard_driver = object
        self._hardware_clock_id = object
        
        self._utils = Utils()

_globals = Globals()