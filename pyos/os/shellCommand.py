#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class ShellCommand:
    """ A command that a user can invoke from the console """
    def __init__(self, function, cmd, desc):
        self.func = function
        self.command = cmd
        self.description = desc
    

