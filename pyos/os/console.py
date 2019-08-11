import curses
from .interrupt import Interrupt
from pyos.globals import _globals

class Console:
	def __init__(self, *args, **kwargs):
		self.x_position = 0
		self.y_position = 0
		self.buffer = ''
		self.screen = object
		self.cmd_history = []
		self.cmd_index = []
		self.curse = curses.wrapper(self._setup)
  	
	def _setup(self, stdscr):
		# reset x and y pos
		self.resetXY()
		# Use the color of the existing terminal
		curses.start_color()
		curses.use_default_colors()
		# Clear screen
		stdscr.clear()
		stdscr.keypad(1)
		self.screen = stdscr
		self.refresh()

	def clear(self):
		self.screen.clear()

	def resetXY(self):
		self.x_position = 0
		self.y_position = 0
	
	def onKeyPress(self, key):
		_globals._kernel_interrupt_queue.enqueue(Interrupt(_globals.KEYBOARD_IRQ, key))

	def refresh(self):
		key = self.screen.getch()
		# while key != ord('q'):
		# must be first
		# self.screen = stdscr
		self.onKeyPress(key)
		# self.write(str(_globals._kernel_interrupt_queue.length()))
		self.screen.refresh() 

	def write(self, string):
		# print(string)
		self.screen.addstr(0,0, string)
		self.screen.refresh() 
			
	# def handleInput(self):
	# 	# while ()