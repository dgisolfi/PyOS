#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.os.commands import shell_commands
from pyos.os.interrupt import Interrupt
from pyos.globals import _globals
import curses

class Console:
	""" The GUI of the OS 
	
	Configures and hides all interactions with the python curses lib
	"""
	
	def __init__(self, *args, **kwargs):
		self.x_position = 0
		self.y_position = 0
		self.buffer = ''
		self.cmd_history = ['']
		self.cmd_suggestions = []
		self.cmd_index = 0
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
		# do not wait for input when calling getch
		screen.nodelay(True)
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

		Parameters
		----------
		key : int
			Unicode code point
		"""
		# When using the non-blocking screen mode, no key 
		# press is denoted by a negative 1
		if key != -1:
			_globals._kernel_interrupt_queue.enqueue(
				Interrupt(_globals.KEYBOARD_IRQ, key)
			)
	
	def newLine(self):
		""" Advances the console by 1 line, handles all bound checking """
		self.x_position = 0
		self.y_position += self.checkBounds('y')
		
	def clearLine(self):
		self.buffer = ''
		while self.x_position > 2:
			self.screen.delch(self.y_position, self.x_position)
			self.x_position -= 1

	def write(self, string:str):
		"""Writes given string to the console

		Parameters
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

		Parameters
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
			# Check to see if it's "special" (enter or ctrl-c) or 
			# "normal" (anything else that the keyboard device driver gave us).
			if char == chr(13): # Enter key
				# The enter key marks the end of a console command, so ... 
				# ... tell the shell ...
				# Add to the command history
				self.cmd_history[-1] = self.buffer
				# adds empty string so the user can go back to typing without deleting cmd
				self.cmd_history.append('')
				self.cmd_index = len(self.cmd_history)-1
				
				_globals._shell.handleInput(self.buffer);
				# ... and reset our buffer.
				self.buffer = ''
			elif char == chr(127) or char == chr(8): # Delete Key
				# the prompt is at pos 1 and the space is at 2 
				# lines start at pos 3
				if self.x_position > 2:
					# this is why python is the best...no long gros syntax
					# just simple string slicing using square brackets
					# For reference the following is the way i did the same thing in TS
					# var lastChar = this.buffer.charAt(this.buffer.length - 1);
                    # this.buffer = this.buffer.substring(0, this.buffer.length - 1);
					self.buffer = self.buffer[:-1]
					self.screen.delch(self.y_position, self.x_position)
					self.x_position -= 1
			elif char == chr(9): # tab
				suggestion = self.cmdCompletion(self.buffer)
				if suggestion is not None:
					remaining_len = len(suggestion) - len(self.buffer)
					rest_of_cmd = suggestion[-remaining_len:]
					self.write(rest_of_cmd)
					self.buffer += rest_of_cmd
			elif char == chr(259): # up
				cmd = self.cmdHistory('up')
				if cmd is not None:
					self.buffer = cmd
					self.x_position = 2
					self.write(self.buffer)
			elif char == chr(258): # down
				cmd = self.cmdHistory('down')
				if cmd is not None:
					self.buffer = cmd
					self.x_position = 2
					self.write(self.buffer)
			elif char == chr(3): # Ctrl-C
				_globals._kernel.krnShutdown(0)
			else:
				# This is a "normal" character, so ...
				# ... draw it on the screen...
				self.write(char)
				# ... and add it to our buffer.
				self.buffer += char;

	def cmdCompletion(self, buffer:str) -> str:
		"""Given the current buffer a possible command will be auto completed 

		Parameters
		----------
		buffer : str
			the current unhandled input stream

		Returns
		-------
		suggestion : str
			A predictions as to what the command the user may be typing
		"""
		# the length of the longest match(s) found
		char_match_len = 0
		for cmd in shell_commands:
			if cmd[1].startswith(buffer):
				if cmd[1] not in self.cmd_suggestions:
					self.cmd_suggestions.append(cmd[1])
		
		if len(self.cmd_suggestions) == 1:
			return self.cmd_suggestions[0]
		else:
			return None
	
	def cmdHistory(self, direction:str) -> str:
		"""Given a direction the command history is cycled

		Parameters
		----------
		direction : str
			the arrow direction the user pressed

		Returns
		-------
		cmd : str
			the command from the history array that is next in the direction specified
		"""
		if len(self.cmd_history) is 0:
			return None
		else:
			self.clearLine()
			num_of_elements = len(self.cmd_history)

			if direction is 'up':
				if (self.cmd_index - 1) != -1:
					self.cmd_index -= 1

			elif direction is 'down':
				if (self.cmd_index + 1) != num_of_elements:
					self.cmd_index += 1
	
			return self.cmd_history[self.cmd_index]