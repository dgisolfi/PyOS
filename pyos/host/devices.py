from pyos.globals import _globals

class Devices:
    def __init__(self):
        _globals._hardware_clock_id = -1

    def hostClockPulse(self):
        # Increment the hardware (host) clock.
        _globals._os_clock += 1
        # Call the kernel clock pulse event handler.
        _globals._kernel.krnOnCPUClockPulse()
        



