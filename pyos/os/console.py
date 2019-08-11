import curses
from .interrupt import Interrupt
from pyos.globals import _globals

class Console:
	def __init__(self, *args, **kwargs):
		self.x_position = 0
		self.y_position = 0
		self.buffer = ''
		self.cmd_history = []
		self.cmd_index = []
		self.curses = curses
		self.screen = self._setup()
			
	def _setup(self):
		# reset x and y pos
		self.resetXY()
		screen = curses.initscr()
		# Use the color of the existing terminal
		curses.start_color()
		curses.use_default_colors()
		curses.noecho()
		# create the screen
		
		# Clear screen
		screen.clear()
		screen.keypad(1)
		
		return screen

	def clear(self):
		self.screen.clear()

	def resetXY(self):
		self.x_position = 0
		self.y_position = 0
	
	def onKeyPress(self, key):
		_globals._kernel_interrupt_queue.enqueue(Interrupt(_globals.KEYBOARD_IRQ, key))

	
	def write(self, string):
		if len(string) == 1:
			self.screen.addch(self.y_position, self.x_position, string)
			self.x_position += 1
			# TODO: check for out of bounds
		else:
			for char in string:
				self.screen.addch(self.y_position, self.x_position, char)
				self.x_position += 1
				# TODO: check for out of bounds
		
		self.screen.refresh()
			
	# def handleInput(self):
	# 	# while ()