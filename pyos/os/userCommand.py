#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class UserCommand:
    """ The users input that will be translated into a shell command """
    def __init__(self, cmd:str, args:list):
        self.command = cmd
        self.args = args
