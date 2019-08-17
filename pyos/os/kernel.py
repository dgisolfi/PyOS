#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.os.keyboardDriver import KeyboardDriver
from pyos.globals import _globals
from pyos.os.console import Console
from pyos.os.queue import Queue
from pyos.os.shell import Shell
import logging
import sys


class Kernel:
    """ OS Startup and Shutdown Routines """
    def __init__(self):
        self.handler = None
        self.logger = self.configLogger()
       

    def configLogger(self):
        """Creates and Configures a python Logger for the OS

        Returns
        -------
        logger
            An instance of a python logger(using the logging lib) 
            that facilitates all kernel tracing
        """
        logger = logging.getLogger('pyos')
        logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler('pyos.log')
        self.handler.setLevel(logging.INFO)
        logger.addHandler(self.handler)
        return logger

    def bootstrap(self):
        """ Loads the initial OS components """

        # Create Global Queues
        # IRQs (Interup Requests)
        _globals._kernel_interrupt_queue = Queue()
        _globals._kernel_buffers = []
        # Device Input to be proccessed
        _globals._kernel_input_queue = Queue()

        # Init Console
        _globals._console = Console()

        # Load the Keyboard Device Driver
        self.krnTrace('Loading the keyboard device driver.')
        # Construct it.
        _globals._krn_keyboard_driver = KeyboardDriver()
        # Call the driverEntry() initialization routine.
        _globals._krn_keyboard_driver.driver_entry()
        self.krnTrace(_globals._krn_keyboard_driver.status)

       
        # Enable the OS Interrupts. 
        self.krnTrace('Enabling the interrupts.');
        self.krnEnableInterrupts()

        # Launch the shell 
        self.krnTrace('Creating and Launching the shell.')
        _globals._shell = Shell()


    def krnShutdown(self, exit_code:int):
        """Unloads drivers and preforms system shutdown

        Attributes
        ----------
        exit_code : int
            the exit code of the OS after shutdown; 0 if okay, 
            greater than 0 otherwise
        """
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
        self.handler.close()
        sys.exit(exit_code)
    
    """ Interrupt Handling """
    def krnEnableInterrupts(self):
        """ Enables all devices to send intterupts """
        # Keyboard
        _globals._devices.hostEnableKeyboardInterrupt();
        # Put more here.
    
    def krnDisableInterrupts(self):
        """ Disables intterupts from all devices """
        # Keyboard
        _globals._devices.hostDisableKeyboardInterrupt();
        # Put more here.

    def krnTrace(self, msg:str):
        """ Logs system level info
        
        Attributes
        ----------
        msg : str
            details to add to log 
        """
        if _globals._trace:
            self.logger.log(logging.INFO, msg)

    def krnTimerISR(self):
        """The built-in TIMER (not clock) Interrupt Service Routine 
        (as opposed to an ISR coming from a device driver). Check 
        multiprogramming parameters and enforce quanta here. 
        Call the scheduler / context switch here if necessary.
        """
        pass

    def krnOnCPUClockPulse(self):
        """Checks the interrupt queue and handles any found before 
        cycling the CPU again. Otherwise logs 'idle' to the log
        """

        if _globals._kernel_interrupt_queue.length() > 0:
            interrupt = _globals._kernel_interrupt_queue.dequeue()
            self.krnInterruptHandler(interrupt.irq, interrupt.params)
        elif _globals._cpu.is_executing:
            _globals._cpu.cycle()
        else:
            self.krnTrace('idle')

    def krnInterruptHandler(self, irq:int, params:list):
        """Invokes the requested Interrupt Service Routine

        Attributes
        ----------
        irq : int
            Number denoting action to be preformed
        params : list
            a list of possible parameters for the action to be invoked
        """
        self.krnTrace(f'Handling IRQ~ {irq}')

        if irq == _globals.TIMER_IRQ:
            self.krnTimerISR()
        elif irq == _globals.KEYBOARD_IRQ:
            _globals._krn_keyboard_driver.isr(params)
            _globals._console.handleInput()

    def krnTrapError(self, msg):
        """Called when OS throws an error, calls 
        shutdown with a proper exit code
        """
        self.krnTrace(f'OS ERROR - TRAP: {msg}')
        # set a 1 as the status as clearly something is wrong
        self.krnShutdown(1)