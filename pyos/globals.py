

class Globals:
    def __init__(self):
        """ global constants """
        self._APP_NAME = 'PyOS'
        # 100 ms
        self._CPU_CLOCK_INTERVAL = 0.01
        self.TIMER_IRQ = 0
        self.KEYBOARD_IRQ = 1

        """ global variables """
        self._cpu = None
        self._os_clock = 0
        # (currently unused)  0 = Kernel Mode, 1 = User Mode
        self._mode = 0

        self._trace = True

        # Os Kernal
        self._kernel = None
        self._kernel_interrupt_queue = None
        self._kernel_input_queue = None
        self._kernel_buffers = []
        
        self._console = None
        self._shell = None

        self._devices = None

        self._sarcastic_mode = False

        self._krn_keyboard_driver = None
        self._hardware_clock_id = None
        


_globals = Globals()