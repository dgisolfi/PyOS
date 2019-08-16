
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

	def execute(self, fn:str, args=None):
		_globals._console.newLine()
		# call the function passed and send its args along as well
		if args is None or len(args) == 0:
			eval(f'{fn}()')
		else:
			# *args
			eval(f'{fn}({(args)})')


		if (_globals._console.x_position > 0):
			_globals._console.newLine()
		self.prompt()


	""" Shell Commands """

	def invalidCommand(self):
		_globals._console.write('Invalid Command. ')
		# TODO: Implement sarcasm mode
		_globals._console.write('Type \'help\' for, well... help.')

	def version(self):
		_globals._console.write(
			f'{_globals._APP_NAME} v{_globals._APP_VERSION}'
		)

	def help(self):
		_globals._console.write('Commands:')
		for cmd in self.command_list:
			_globals._console.newLine()
			_globals._console.write(f' {cmd.command} {cmd.description}')

	def shutdown(self):
		_globals._console.write('Shutting down...')
		# call kernal routine, pass in 0 as status, this is a normal shutdown
		_globals._kernel.krnShutdown(0)

	def cls(self):
		_globals._console.clear()
		_globals._console.resetXY()

	def man(self):
		pass

	def trace(self):
		pass

	def rot13(self):
		pass

	def setPrompt(self):
		pass