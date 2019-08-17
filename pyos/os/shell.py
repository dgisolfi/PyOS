#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from .shellCommand import ShellCommand
from .userCommand import UserCommand
from .commands import shell_commands
from pyos.globals import _globals

class Shell:
	def __init__(self):
		self.prompt_str = '❯'
		self.command_list = []
		self.curses = '[fuvg],[cvff],[shpx],[phag],[pbpxfhpxre],[zbgureshpxre],[gvgf]'
		self.apologies = '[sorry]'
		self.loadCmds()
		self.prompt()
	
	""" Load the command list. """
	def loadCmds(self):
		for cmd in shell_commands:
			self.command_list.append(
				ShellCommand(cmd[0],cmd[1],cmd[2])
			)

	def prompt(self):
		_globals._console.write(self.prompt_str)
		_globals._console.write(' ')

	def handleInput(self, buffer):
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
			# TODO: implement curse checking...
			self.execute('self.invalidCommand')

	def parseInput(self, buffer) -> UserCommand:
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
		_globals._console.newLine()
		# call the function passed and send its args along as well
		eval(f'{fn}({args})')
		if (_globals._console.x_position > 0):
			_globals._console.newLine()
		self.prompt()

	""" Shell Commands """

	def invalidCommand(self, args):
		_globals._console.write('Invalid Command. ')
		# TODO: Implement sarcasm mode
		_globals._console.write('Type \'help\' for, well... help.')

	# TODO: as a part of sarcastic mode....
	def shellCurse():
		pass

	def shellApology():
		pass

	def version(self, args):
		_globals._console.write(
			f'{_globals._APP_NAME} v{_globals._APP_VERSION}'
		)

	def help(self, args):
		_globals._console.write('Commands:')
		for cmd in self.command_list:
			_globals._console.newLine()
			_globals._console.write(f' {cmd.command} {cmd.description}')

	def shutdown(self, args):
		_globals._console.write('Shutting down...')
		# call kernal routine, pass in 0 as status, this is a normal shutdown
		_globals._kernel.krnShutdown(0)

	def cls(self, args):
		_globals._console.clear()
		_globals._console.resetXY()

	def man(self, args):
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
				

	def trace(self, args):
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
				

	def rot13(self, args):
		if len(args) > 0:
			_globals._console.write(
				f'{" ".join(args)} = "{_globals._utils.rot13(" ".join(args))}"'
				)
		else:
			_globals._console.write(
				'Usage: rot13 <string>  Please supply a string.'
				)

	def setPrompt(self, args):
		if len(args) > 0:
			self.prompt_str = args[0]
		else:
			_globals._console.write(
				'Usage: prompt <string>  Please supply a string.'
			)