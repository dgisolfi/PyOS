#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.os.interrupt import Interrupt
from pyos.globals import _globals

class CPU:
    """ The simulated CPU that runs 6502 opcodes """
    def __init__(self):
        self.pc = 0
        self.ir = '00'
        self.acc = 0
        self.x_reg = 0
        self.y_reg = 0
        self.z_flag = 0
        self.is_executing = False
        self.instruction_set = {
            'A9' : self.loadAccConst,
            'AD' : self.loadAccMem,
            '8D' : self.storeAccMem,
            '6D' : self.addToAcc,
            'A2' : self.loadXRegConst,
            'AE' : self.loadXRegMem,
            'A0' : self.loadYRegConst,
            'AC' : self.loadYRegMem,
            'EA' : self.noOP,
            '00' : self.progBreak,
            'EC' : self.xRegCompare,
            'DO' : self.branch,
            'EE' : self.incByte,
            'FF' : self.sysCallPrint
        }
    
    def cycle(self):
        """ Preforms a single opcode operation per cycle called """
        _globals._kernel.krnTrace('CPU cycle')
        
        # get the base and limit of the running proccess
        base = _globals._pcm.running_process.base
        limit = _globals._pcm.running_process.limit

        # FETCH
        self.ir = _globals._memory_accessor.read(self.pc)

        # DECODE/EXECUTE
        self.execute(self.ir)

        # update the PCB for the proccess to the current CPU values
        _globals._pcm.running_process.pc = self.pc
        _globals._pcm.running_process.ir = self.ir
        _globals._pcm.running_process.acc = self.acc
        _globals._pcm.running_process.x_reg = self.x_reg
        _globals._pcm.running_process.y_reg = self.y_reg
        _globals._pcm.running_process.z_flag = self.z_flag

        # Check if proccess has completed
        if self.pc + base >= limit:
            # terminate 
            _globals._pcm.running_process.state = 'terminated'
            _globals._kernel_interrupt_queue.enqueue(
                Interrupt(
                    _globals.PROCESS_EXIT, 
                    _globals._pcm.runningprocess.pid
                )
            )

    """ Helper Methods """
    def execute(self, op_code:str):
        if op_code not in self.instruction_set.keys():
            _globals._console.write(f'Invalid Op Code: {op_code}, Exiting process.')
            _globals._kernel_interrupt_queue.enqueue(
                Interrupt(
                    _globals.PROCESS_EXIT, 
                    _globals._pcm.runningprocess.pid
                )
            )
        else:
            # _globals._console.write(str(self.instruction_set[op_code.upper()]))
            self.instruction_set[op_code.upper()]()

    def incPC(self, num):
        self.pc += num

    def decimal(self, hex:str):
        return int(hex, 16)

    def hex(self, decimal:str):
        return ("0x%02X" % decimal).upper()[2:]

    """ Op Codes """
    # A9 -- Load the accumulator with a constant
    def loadAccConst(self):
        self.acc = self.decimal(
            _globals._memory_accessor.read(self.pc+1)
        )
        _globals._console.write(str(self.acc))
        self.incPC(2)

    # AD -- Load the accumulator from memory
    def loadAccMem(self):
        # Store the values at the first and second postions
        val1 = _globals._memory_accessor.read(self.pc+1)
        val2 = _globals._memory_accessor.read(self.pc+1)
        # Switch the order because we must read/write in little endian
        addr = val2 + val1
        # Read from memory with the corected endian format 
        value = _globals._memory_accessor.read(
            (self.decimal(addr))
        )
        # Finally, parse it from HEX to Decimal and load the Accumulator
        self.acc = self.decimal(value)

        self.incPC(3)

    # 8D -- Store the accumulator in memory
    def storeAccMem(self):
        # Store the values at the first and second postions
        val1 = _globals._memory_accessor.read(self.pc+1)
        val2 = _globals._memory_accessor.read(self.pc+1)
        # Switch the order because we must read/write in little endian
        addr = val2 + val1
        value = self.hex(self.acc).upper()
        _globals._memory_accessor.write(self.decimal(addr), value)
        
        self.incPC(3)

    # 6D -- Read from memory and add to the accumulator
    def addToAcc(self):
        # Store the values at the first and second postions
        val1 = _globals._memory_accessor.read(self.pc+1)
        val2 = _globals._memory_accessor.read(self.pc+1)
        # Switch the order because we must read/write in little endian
        addr = val2 + val1
        # Read from memory with the corected endian format 
        value = _globals._memory_accessor.read(
            (self.decimal(addr))
        )

        # Finally, parse it from HEX to Decimal and add it to the Accumulator
        self.acc += self.decimal(value)

        self.incPC(3)

    # A2 -- Load the x register with a given constant
    def loadXRegConst(self):
        pass

    # AE -- Load the x register from memory
    def loadXRegMem(self):
        pass

    # A0 -- Load the y register with a given constant
    def loadYRegConst(self):
        pass

    # AC -- Load the y register from memory
    def loadYRegMem(self):
        pass

    # EA -- No Operation
    def noOP(self):
        pass

    # 00 -- break
    def progBreak(self):
        _globals._kernel_interrupt_queue.enqueue(
            Interrupt(
                _globals.PROCESS_EXIT, 
                _globals._pcm.running_process.pid
            )
        )

    # EC -- Take a byte from memory and compare it 
    # with the x Register...if equal z flag is 0
    def xRegCompare(self):
        pass

    # D0 -- if Z flag is 0, branch x number of bytes
    def branch(self):
        pass

    # EE -- Increment the value of a byte
    def incByte(self):
        pass

    # FF -- System Call...print
    def sysCallPrint(self):
        pass