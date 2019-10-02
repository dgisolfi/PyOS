#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals
from pyos.os.queue import Queue
from pyos.os.pcb import PCB

class ProcessManager:
	""" Stores the state of a process """
	def __init__(self):
		self.pid_counter = 0
		self.resident_queue = {}
		self.ready_queue = {}
		self.terminated_queue = {}
		self.running_process = PCB(-1, 0, 0, 'memory')

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

		process = PCB(self.pid_counter, base, limit, 'memory')
		# put process in resident queue
		process.state = 'resident'
		self.resident_queue[self.pid_counter] = process
		self.pid_counter += 1
		return process.pid

	def exec(self, pid:int=None):
		""" Given a valid pid, that process is run

		Parameters
		----------
		pid : int
			valid process id
		"""
		if pid == None:
			# setup scheduling
			pass

		# Move the process from the ready Queue to the CPU
		self.running_process = self.ready_queue[pid]
		del self.ready_queue[pid]
		self.loadProcessState()
		self.running_process.state = 'running'
		
		_globals._cpu.is_executing = True
		
	def loadProcessState(self):
		_globals._cpu.pc = self.running_process.pc
		_globals._cpu.ir = self.running_process.ir
		_globals._cpu.acc = self.running_process.acc
		_globals._cpu.x_reg = self.running_process.x_reg
		_globals._cpu.y_reg = self.running_process.y_reg
		_globals._cpu.z_flag = self.running_process.z_flag

	def terminate(self, pid: int):
		""" Halts the specifed proccess
		"""

		_globals._console.newLine()
		_globals._console.write(f'process {pid} finished')
		_globals._console.newLine()
		_globals._shell.prompt()


		# reset the nessecary memory segment
		if self.running_process.base == 0:
			_globals._memory_manager.wipeSeg00()
		elif self.running_process.base == 256:
			_globals._memory_manager.wipeSeg01()
		elif self.running_process.base == 513:
			_globals._memory_manager.wipeSeg02()

		
		if str(pid) in self.resident_queue:
			self.terminated_queue[pid] = self.resident_queue[pid]
			self.terminated_queue[pid].state = 'terminated'
			del self.resident_queue[pid]
		elif str(pid) in self.ready_queue.keys():
			self.terminated_queue[pid] = self.ready_queue[pid]
			self.terminated_queue[pid].state = 'terminated'
			del self.ready_queue[pid]
		elif pid == self.running_process.pid:
			self.terminated_queue[pid] = self.running_process
			self.terminated_queue[pid].state = 'terminated'
		else:
			_globals._kernel.krnTrace(f'Termination Error: {pid} not found')
			return

		_globals._cpu.is_executing = False
		self.running_process = PCB(-1, 0, 0, 'memory')