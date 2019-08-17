#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals
from pyos.os.commands import shell_commands
from pyos.os.userCommand import UserCommand
from pyos.os.shellCommand import ShellCommand

class Shell:
	""" Main interaction with OS via CLI """
	def __init__(self):
		self.prompt_str = '❯'
		self.command_list = []
		self.curses = '[fuvg],[cvff],[shpx],[phag],[pbpxfhpxre],[zbgureshpxre],[gvgf]'
		self.apologies = '[sorry]'
		self.loadCmds()
		self.prompt()
	

	def loadCmds(self):
		""" Load the command list. """
		for cmd in shell_commands:
			self.command_list.append(
				ShellCommand(cmd[0],cmd[1],cmd[2])
			)

	def prompt(self):
		""" writes the defined prompt char """
		_globals._console.write(f'{self.prompt_str} ')

	def handleInput(self, buffer:str):
		"""Called by console when the Enter key is pressed

		Attributes
		----------
		buffer : str
			All keyboard inputs in order added by the Keyboard Driver
		"""
		_globals._kernel.krnTrace(f'Shell Command~ {buffer}')
		# parse input
		user_command = self.parseInput(buffer)
		cmd = user_command.command
		args = user_command.args

		# Determine the command and execute it.
		dex = 0
		found = False
		fn = None
		while not found and dex < len(self.command_list):
			# is this the command entered??
			if self.command_list[dex].command == cmd:
				# yup! end the loop and exec it
				found = True
				fn = self.command_list[dex].func
			else:
				dex += 1
		
		if found:
			self.execute(fn, args)
		else:
			# It's not found, so check for curses and 
			# apologies before declaring the command invalid.

			# Check for curses.
			if self.curses.find(f'[{_globals._utils.rot13(cmd)}]') != -1:
				self.execute('self.curse')
			# Check for apologies.
			elif self.apologies.find(f'[{cmd}]') != -1:
				self.execute('self.apology')
			else:
				self.execute('self.invalidCommand')

	def parseInput(self, buffer) -> UserCommand:
		"""Seperates the shell buffer into a command and its args

		Attributes
		----------
		buffer : str
			All keyboard inputs in order added by the Keyboard Driver
		
		Returns
		-------
		object : UserCommand
			holds all parsed arguments and the command itself
		"""
		# remove leading and trailing spaces
		buffer = buffer.strip()
		# Lower case it
		buffer = buffer.lower()
		# split on space to find cmd and args
		buffer = buffer.split(' ')
		# the first element is the cmd, remove it and save the args in its arr
		cmd = buffer.pop(0).strip()
		args = []
		for arg in buffer:
			if arg.strip() != '':
				args.append(arg)
		
		return UserCommand(cmd, args)

	def execute(self, fn:str, args=[]):
		"""Given a string evaluates that string as a function call

		Attributes
		----------
		fn : str
			the full name of a function to be called, EX: 'self.help'
		args : list
			The full list of arguments needed for the function, 
			will default to empty list if not passed
		"""
		_globals._console.newLine()
		# call the function passed and send its args along as well
		eval(f'{fn}({args})')

		if (_globals._console.x_position > 0):
			_globals._console.newLine()
		self.prompt()

	""" Shell Commands """

	def invalidCommand(self, args:list):
		"""Alerts the user that the command entered does 
		not match any command loaded

		All attributes should be placed in the args list
		"""
		_globals._console.write('Invalid Command. ')
		if _globals._sarcastic_mode:
			_globals._console.write('Unbelievable. You, [subject name here],')
			_globals._console.newLine()
			_globals._console.write(
				'must be the pride of [subject hometown here].'
			)
		else:
			_globals._console.write('Type \'help\' for, well... help.')

	def curse(self, args:list):
		""" Reacts appropriately when shots have been fired """
		_globals._console.write(
			'Oh, so that\'s how it\'s going to be, eh? Fine.'
		)
		_globals._console.newLine()
		_globals._console.write('Bitch.')
		_globals._sarcastic_mode = True

	def apology(self, args:list):
		""" handles apologies from user"""
		if _globals._sarcastic_mode:
			_globals._console.write(
				'I think we can put our differences behind us.'
			)
			_globals._console.newLine()
			_globals._console.write(
				'For science . . . You monster.'
			)
			_globals._sarcastic_mode = False
		else:
			_globals._console.write('For what?')
			
	def version(self, args:list):
		"""Displays the app name and version number to the user

		All attributes should be placed in the args list
		"""
		_globals._console.write(
			f'{_globals._APP_NAME} v{_globals._APP_VERSION}'
		)

	def help(self, args:list):
		"""Displays full list of commands and descriptions to user

		All attributes should be placed in the args list
		"""
		_globals._console.write('Commands:')
		for cmd in self.command_list:
			_globals._console.newLine()
			_globals._console.write(f' {cmd.command} {cmd.description}')

	def shutdown(self, args:list):
		"""Preforms controlled system shutdown

		All attributes should be placed in the args list
		"""
		_globals._console.write('Shutting down...')
		# call kernal routine, pass in 0 as status, this is a normal shutdown
		_globals._kernel.krnShutdown(0)

	def cls(self, args:list):
		"""Clears the console window

		All attributes should be placed in the args list
		"""
		_globals._console.clear()
		_globals._console.resetXY()

	def man(self, args:list):
		"""Displays the manuel for a given command

		All attributes should be placed in the args list

		Attributes
		----------
		topic : str
			the name of the command that the manuel should be shown for
		"""
		if len(args) > 0:
			topic = args[0]
			if topic == 'help':
				_globals._console.write(
					'Help displays a list of (hopefully) valid commands.'
				)
			# TODO: Make descriptive MANual page entries for the 
			# the rest of the shell commands here.
			else:
				_globals._console.write(
					f'No manual entry for {args[0]}.'
				)
		else:
			_globals._console.write(
				'Usage: man <topic>  Please supply a topic.'
			)

	def trace(self, args:list):
		"""Sets the boolean for kernel tracing

		All attributes should be placed in the args list

		Attributes
		----------
		setting : str
			either 'on' or 'off'
		"""
		if len(args) > 0:
			setting = args[0]
			if setting == 'on':
				if _globals._trace and _globals._sarcastic_mode:
					_globals._console.write('Trace is already on, doofus.')
				else:
					_globals._trace = True
					_globals._console.write('Trace ON')
			elif setting == 'off':
				_globals._trace = False
				_globals._console.write('Trace OFF')
			else:
				_globals._console.write(
					'Invalid arguement.  Usage: trace <on | off>.'
				)
		else:
			_globals._console.write('Usage: trace <on | off>')
				
	def rot13(self, args:list):
		"""Calls the rot13 utility for the user on specified text

		Attributes
		----------
		string : str
			the string to be rearanged
		"""
		if len(args) > 0:
			_globals._console.write(
				f'{" ".join(args)} = "{_globals._utils.rot13(" ".join(args))}"'
				)
		else:
			_globals._console.write(
				'Usage: rot13 <string>  Please supply a string.'
				)

	def setPrompt(self, args:list):
		"""Sets the prompt of the shell to a user specified string

		All attributes should be placed in the args list

		Attributes
		----------
		prompt : str
			the new set of chars to set the prompt to
		"""
		if len(args) > 0:
			self.prompt_str = args[0]
		else:
			_globals._console.write(
				'Usage: prompt <string>  Please supply a string.'
			)