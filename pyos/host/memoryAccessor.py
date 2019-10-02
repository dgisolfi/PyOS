#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.os.interrupt import Interrupt
from pyos.os.pcb import PCB
from pyos.globals import _globals
from typing import List

@_globals._utils.singleton
class MemoryAccessor:
    """ Manages all segments of memory and enforces boundaries """

    def read(self, address:str) -> str:
        """Given a memory addres the value stored at 
        the addr is returned

        Parameters
        ----------
        address : str
            The hex address of memory to read
        Returns
        -------
        value : str
            The value stored at the hex address
        """
        location = (_globals._pcm.running_process.base + address)
        self.checkBounds(location)
        return _globals._mem.memory[location]

    def readBlock(self, process:PCB) -> List[str]:
        """ Returns the assigned block of memory for a Proccess

        Parameters
        ----------
        proccess : PCB
            The process control block
        Returns
        -------
        block : List[str]
            The full block of memory assigned to the proccess
        """
        return _globals._mem.memory[process.base:process.limit]

    def write(self, address:str, value:str):
        """ Writes a value to a address in memory

        Parameters
        ----------
        address : str
            The hex address of memory to write to
        value : str
            The hex value to write to memory

        Returns
        -------
        Exception
            returns if the hex value is invalid
        """
        location = (_globals._pcm.running_process.base + address)
        if len(value) > 2:
            return Exception(
                'The value must be a 2 char Hex value'
                + 'to be written to memory'
                )

        self.checkBounds(location)
        if len(value) == 1:
            value = f'0{value}'
        
        _globals._mem.memory[location] = value

    def checkBounds(self, location):
        """ Given a memory address an out of bounds check 
        is preformed for the running process
        """
        if location < _globals._pcm.running_process.base:
            _globals._kernel_interrupt_queue.enqueue(
                Interrupt(
                    _globals.OUT_OF_BOUNDS, 
                    _globals._pcm.running_process.pid
                )
            )

        if location > _globals._pcm.running_process.limit:
            _globals._kernel_interrupt_queue.enqueue(
                Interrupt(
                    _globals.OUT_OF_BOUNDS, 
                    _globals._pcm.running_process.pid
                )
            )