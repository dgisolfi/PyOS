#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals
from pyos.host.devices import Devices
from pyos.os.kernel import Kernel
from pyos.host.cpu import CPU
import time

def main():
    """ Initializes the main classes for bootstrap """
    _globals._devices = Devices()
    _globals._cpu = CPU()
    _globals._kernel = Kernel()
    _globals._kernel.bootstrap()

    """ This is the main 'Event Loop' for the OS """
    while True:
        time.sleep(_globals._CPU_CLOCK_INTERVAL)
        _globals._devices.hostClockPulse()

        # This doesnt belong here per se however if placed in 
        # a lower loop the key will not be passsed to the console
        key = _globals._console.screen.getch()
        _globals._console.onKeyPress(key)
    
if __name__ == "__main__":
    main()