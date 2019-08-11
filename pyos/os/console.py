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
		self.height = int
		self.width = int
		self.screen = self._setup()
			
	def _setup(self):
		# reset x and y pos
		self.resetXY()
		# create the screen
		screen = curses.initscr()
		# Use the color of the existing terminal
		curses.start_color()
		curses.use_default_colors()
		curses.noecho()
		# get the height and with of the screen to 
		# avoid curses errors on write
		self.height, self.width = screen.getmaxyx()
		# setup scrolling
		screen.scrollok(True)
		screen.setscrreg(0, self.height-1)
		# screen.idlok(True)
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
			pos = self.checkBounds('x')
			self.x_position += pos
			self.screen.addch(self.y_position, self.x_position, string)

		else:
			for char in string:
				self.screen.addch(self.y_position, self.x_position, char)
				self.x_position += 1
				# TODO: check for out of bounds
		
		self.screen.refresh()
	
	def checkBounds(self, dim):
		if dim.lower() == 'x':
			if (self.x_position+1) == self.width:
				self.y_position += self.checkBounds('y')
				return -(self.width-1)
			else:
				return 1
		elif dim.lower() == 'y':
			new = self.y_position + 1
			_globals._kernel.krnTrace(f'before: {self.y_position}, after: {new}, max: {self.height}')
			if (self.y_position+1) == self.height:
				# We have hit the bottom of the terminal,
				# we need to scroll
				self.scroll()
			
			return 1

		else:
			raise ValueError(f'Dimension: {dim} not valid, must be X or Y')
			
	def scroll(self):
		self.screen.scroll()