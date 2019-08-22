#!/usr/bin/env python3
# Daniel Nicolas Gisolfi
from pyos.globals import _globals

@_globals._utils.singleton
class Memory:
	""" Serves as main memory for host """
	def __init__(self):
		self._memory = []
		self.is_seg_00_full = False
		self.is_seg_01_full = False
		self.is_seg_02_full = False
		self._setup()

	def __getitem__(self, key):
		return self._memory[key]

	def __setitem__(self, key, value):
		self._memory[key] = value
		
	def _setup(self):
		[ self.memory.append('00') for i in range(0,767) ]
	
	@property
	def memory(self) -> list:
		return self._memory

	@memory.setter
	def memory(self, value:list):
		self._memory = value

	@memory.deleter
	def memory(self):
		del self._memory

	def append(self, element:object):
		self._memory.append(element)