from .queue import Queue
from .console import Console
from .shell import Shell
from .keyboardDriver import KeyboardDriver
from pyos.globals import _globals
import logging
import sys

# TODO: This is ugly put this inside the class 
logging.basicConfig(
    filename='pyos.log', 
    level=logging.INFO
)

class Kernel:
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

       
        """ Enable the OS Interrupts. """
        self.krnTrace('Enabling the interrupts.');
        self.krnEnableInterrupts()

        """ Launch the shell """
        self.krnTrace('Creating and Launching the shell.')
        _globals._shell = Shell()


    def krnShutdown(self, status):
        self.krnTrace('Begin shutdown OS');
        # TODO: Check for running processes.  If there are some, alert and stop. Else...
        # ... Disable the Interrupts.
        self.krnTrace('Disabling the interrupts.');
        self.krnDisableInterrupts();
        #
        # Unload the Device Drivers?
        # More?
        #
        self.krnTrace('End shutdown OS');
        sys.exit(status)
    
    """ Interrupt Handling """
    def krnEnableInterrupts(self):
        # Keyboard
        _globals._devices.hostEnableKeyboardInterrupt();
        # Put more here.
    
    def krnDisableInterrupts(self):
        # Keyboard
        _globals._devices.hostDisableKeyboardInterrupt();
        # Put more here.

    def krnTrace(self, msg):
        if _globals._trace:
            logging.info(msg)

    def krnTimerISR(self):
        # The built-in TIMER (not clock) Interrupt Service Routine 
        # (as opposed to an ISR coming from a device driver). Check 
        # multiprogramming parameters and enforce quanta here. 
        # Call the scheduler / context switch here if necessary.
        pass

    def krnOnCPUClockPulse(self):
        if _globals._kernel_interrupt_queue.length() > 0:
            interrupt = _globals._kernel_interrupt_queue.dequeue()
            self.krnInterruptHandler(interrupt.irq, interrupt.params)
        # elif _globals._cpu.is_executing:
        #     _globals._cpu.cycle()
        else:
            self.krnTrace('idle')

    def krnInterruptHandler(self, irq, params):
        self.krnTrace(f'Handling IRQ~ {irq}')

        if irq == _globals.TIMER_IRQ:
            self.krnTimerISR()
        elif irq == _globals.KEYBOARD_IRQ:
            _globals._krn_keyboard_driver.isr(params)
            _globals._console.handleInput()

    def krnTrapError(self, msg):
        self.krnTrace(f'OS ERROR - TRAP: {msg}')
        # set a 1 as the status as clearly something is wrong
        self.krnShutdown(1)