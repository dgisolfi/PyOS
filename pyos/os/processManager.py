#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals
from pyos.os.queue import Queue
from pyos.os.pcb import PCB

class ProcessManager:
	""" Stores the state of a process """
	def __init__(self):
		self.pid_counter = 0
		self.resident_queue = {};
		self.ready_queue = {};
		self.terminated_queue = {};
		self.running_process = PCB(-1, 0, 0, 0, 'memory')

	def create(self, base:int, limit:int) -> int:
		""" Creates a new process and adds it to the resident queue
		
		Parameters
		----------
		base : int
			starting index in memory of the program
		limit : int
			ending index in memory of the program

		Returns
		-------
		pid : int
			process id of new process
		"""

		process = PCB(self.pid_counter, base, limit)
		# put process in resident queue
		process.state = 'resident'
		self.resident_queue[self.pid_counter] = process
		self.pid_counter += 1
		return process.pid

	def exec(self, pid:int):
		""" Given a valid pid, that process is run

		Parameters
		----------
		pid : int
			valid process id
		"""

		# Move the process from the ready Queue to the CPU
		self.running_process = self.ready_queue[pid]
		del self.ready_queue[pid]
		self.loadProcessState()
		
	def loadProcessState(self):
		_globals._cpu.pc = self.running_process.pc
		_globals._cpu.ir = self.running_process.ir
		_globals._cpu.acc = self.running_process.acc
		_globals._cpu.x_reg = self.running_process.x_reg
		_globals._cpu.y_reg = self.running_process.y_reg
		_globals._cpu.z_flag = self.running_process.z_flag

