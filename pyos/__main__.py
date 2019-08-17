#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

import time
from pyos.os import Kernel
from pyos.globals import _globals
from pyos.host import Devices
from pyos.host import CPU


def main():
    _globals._devices = Devices()
    _globals._cpu = CPU()
    _globals._kernel = Kernel()
    _globals._kernel.bootstrap()
    
    while True:
        time.sleep(_globals._CPU_CLOCK_INTERVAL)
        _globals._devices.hostClockPulse()

        key = _globals._console.screen.getch()
        _globals._console.onKeyPress(key)
    
    

if __name__ == "__main__":
    main()