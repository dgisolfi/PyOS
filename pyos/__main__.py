#!/usr/bin/env python3
import time
from pyos.os import Kernel
from pyos.globals import _globals
from pyos.host import Devices


def main():
    _globals._kernel = Kernel()
    
    _globals._kernel.bootstrap()
    devices = Devices()

    while True:
        time.sleep(_globals._CPU_CLOCK_INTERVAL)
        devices.hostClockPulse()

        key = _globals._console.screen.getch()
        _globals._console.onKeyPress(key)
    
    

if __name__ == "__main__":
    main()