#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class Utils:
    """ This class holds all external utilities that 
    doent nessecarily belong in the OS
    """
    def rot13(self, string:str) -> str:
        """A simple implementation of the ROT13 cipher

        Parameters
        ----------
        string : str
            the string to be shifted

        Returns
        -------
        shifted : str
            the shifted result of the cipher
        """
        shifted = ''
        for char in string:
            # Convert to number with ord.
            num = ord(char)
            # preform shift
            #         'a'           'z'
            if num >= 97 and num <= 122:
                #        'm'
                if num > 109:
                    num -= 13
                else:
                    num += 13
            #          'A'           'Z'
            elif num >= 65 and num <= 90:
                #        'M'
                if num > 77:
                    num -= 13
                else:
                    num += 13

            # build result
            shifted += chr(num)
        return shifted

    def singleton(self, class_):
        instances = {}
        def getinstance(*args, **kwargs):
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
            return instances[class_]
        return getinstance