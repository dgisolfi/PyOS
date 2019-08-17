#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

"""Add to this array to when new shell commands are added

Each new command takes the form of an array with 3 elements

element 0 -> exact name of method to be called in the shell class

element 1 -> the command the user types in   

element 2 -> Short Description of what it does

"""
shell_commands = [
    ['self.version', 'ver', '- Displays the current version data.'],
    ['self.help', 'help', '- This is the help command. Seek help.'],
    ['self.shutdown', 'shutdown', '- Shuts down the virtual OS but '
    'leaves the underlying host / hardware simulation running.'],
    ['self.cls', 'cls', '- Clears the screen and resets the cursor position.'],
    ['self.man', 'man', '<topic> - Displays the MANual page for <topic>.'],
    ['self.trace', 'trace', '<on | off> - Turns the OS trace on or off.'],
    ['self.rot13', 'rot13', '<string> - Does rot13 obfuscation on <string>.'],
    ['self.setPrompt', 'prompt', '<string> - Sets the prompt.']
]