#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class PCB:
	""" Stores the state of a process """
	def __init__(self, pid, base, limit, location):
		self.pid = pid
		self.base = base
		self.limit = limit
		self.location = location
		self.state = 'resident'
		self.pc = 0
		self.acc = 0
		self.ir = '00'
		self.x_reg = 0
		self.y_reg = 0
		self.z_flag = 0
		self.turnaround_time = 0
		self.wait_time = 0
