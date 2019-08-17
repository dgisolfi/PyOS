#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

class Utils:
    def rot13(self, string:str) -> str:
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