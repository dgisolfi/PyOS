#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals
from pyos.os.interrupt import Interrupt
import curses

class Console:
	""" The GUI of the OS 
	
	Configures and hides all interactions with the python curses lib
	"""
	
	def __init__(self, *args, **kwargs):
		self.x_position = 0
		self.y_position = 0
		self.buffer = ''
		self.cmd_history = []
		self.cmd_index = []
		self.curses = curses
		self.height = int
		self.width = int
		self.screen = self._setup()
			
	def _setup(self):
		""" Preforms needed setup returns a new curses window instance """
		# reset x and y pos
		self.resetXY()
		# create the screen
		screen = curses.initscr()
		# Use the color of the existing terminal
		curses.start_color()
		curses.use_default_colors()
		curses.noecho()
		# disable newline mode
		curses.nl(False)
		# enables raw mode so we can handle all key codes ourselves
		curses.raw(True)
		# get the height and with of the screen to 
		# avoid curses errors on write
		self.height, self.width = screen.getmaxyx()
		# setup scrolling
		screen.scrollok(True)
		# screen.setscrreg(0, self.height-1)
		# screen.idlok(1)
		# Clear screen
		screen.clear()
		return screen

	def clear(self):
		""" Wraps the clear method of the curses window """
		self.screen.clear()

	def resetXY(self):
		""" It does exactly what you think it does... """
		self.x_position = 0
		self.y_position = 0
	
	def onKeyPress(self, key: int):
		"""Queues a new Interrupt for each key press

		Attributes
        ----------
		key : int
			Unicode code point
		"""
		_globals._kernel_interrupt_queue.enqueue(
			Interrupt(_globals.KEYBOARD_IRQ, key)
		)
	
	def newLine(self):
		""" Advances the console by 1 line, handles all bound checking """
		self.x_position = 0
		self.y_position += self.checkBounds('y')
		
	
	def write(self, string:str):
		"""Writes given string to the console

		Attributes
        ----------
		string : str
			string or char to be written to screen
		"""
		if string is '':
			return
		if len(string) == 1:
			self.x_position += self.checkBounds('x')
			self.screen.addch(self.y_position, self.x_position, string)
		else:
			for char in string:
				self.x_position += self.checkBounds('x')
				self.screen.addch(self.y_position, self.x_position, char)
		self.screen.refresh()
	
	def checkBounds(self, dim:str) -> int:
		"""Preforms bounds checking for curses window

		Attributes
        ----------
		dim : str
			either the x or y dimension, pass 'x' or 'y' to preform check

		Raises
		------
		Dimension: not valid
			The given string does not match either dimension
		Returns
		-------
		int
			number to increment the dim by to stay within bounds
		"""
		if dim.lower() == 'x':
			if (self.x_position+1) == self.width:
				self.y_position += self.checkBounds('y')
				return -(self.width-1)
			else:
				return 1
		elif dim.lower() == 'y':
			new = self.y_position + 1
			if (self.y_position+1) == self.height:
				# We have hit the bottom of the terminal,
				# we need to scroll
				self.screen.scroll()
			return 1
		else:
			raise ValueError(f'Dimension: {dim} not valid, must be X or Y')


	def handleInput(self):
		"""Handles the kernel input queue

		Will dequeue characters one at a time and deal with them accordingly.
		"""
		while (_globals._kernel_input_queue.length() > 0):
			# Get the next character from the kernel input queue.
			char = _globals._kernel_input_queue.dequeue()
			# Check to see if it's "special" (enter or ctrl-c) or "normal" (anything else that the keyboard device driver gave us).
			if char == chr(13): # Enter key
				# The enter key marks the end of a console command, so ... 
				# ... tell the shell ...
				self.write(char)
				_globals._shell.handleInput(self.buffer);
				# ... and reset our buffer.
				self.buffer = ''
			elif char == chr(3): # Ctrl-C
				_globals._kernel.krnShutdown(0)
			else:
				# This is a "normal" character, so ...
				# ... draw it on the screen...
				self.write(char)
				# ... and add it to our buffer.
				self.buffer += char;