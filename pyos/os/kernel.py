from .queue import Queue
from .console import Console
from .keyboardDriver import KeyboardDriver
from pyos.globals import _globals


class Kernel:
    def __init__(self):
        pass

    def bootstrap(self):
        """ Create Global Queues """
        # IRQs (Interup Requests)
        _globals._kernel_interrupt_queue = Queue()
        _globals._kernel_buffers = []
        # Device Input to be proccessed
        _globals._kernel_input_queue = Queue()

        """ Init Console """
        _globals._console = Console()

        """ Load the Keyboard Device Driver """
        self.krnTrace('Loading the keyboard device driver.')
        # Construct it.
        _globals._krn_keyboard_driver = KeyboardDriver()
        # Call the driverEntry() initialization routine.
        _globals._krn_keyboard_driver.driver_entry()
        self.krnTrace(_globals._krn_keyboard_driver.status)


    def krnTrace(self, msg):
        if _globals._trace:
            pass
            # _globals._console.write(msg)
            # print(msg)

    def krnTimerISR(self):
        # The built-in TIMER (not clock) Interrupt Service Routine (as opposed to an ISR coming from a device driver).
        # Check multiprogramming parameters and enforce quanta here. Call the scheduler / context switch here if necessary.
        pass

    def krnOnCPUClockPulse(self):
        _globals._console.refresh()
        # _globals._console.write(str(_globals._kernel_interrupt_queue.length()))
        if _globals._kernel_interrupt_queue.length() > 0:
            interrupt = _globals._kernel_interrupt_queue.dequeue()
            self.krnInterruptHandler(interrupt.irq, interrupt.params)
        # elif _globals._cpu.is_executing:
        #     _globals._cpu.cycle()
        else:
            self.krnTrace('idle') #

    def krnInterruptHandler(self, irq, params):
        self.krnTrace(f'Handling IRQ~ {irq}')


        if irq == _globals.TIMER_IRQ:
            self.krnTimerISR()
        elif irq == _globals.KEYBOARD_IRQ:
            _globals._krn_keyboard_driver.isr(params)
            # _stdin.handleInput()