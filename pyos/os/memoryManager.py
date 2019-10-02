#!/usr/bin/env python3
# Daniel Nicolas Gisolfi

from pyos.globals import _globals

@_globals._utils.singleton
class MemoryManager:
    """ Manages main interactions with host Memory """
    def loadInMem(self, code:list) -> tuple:
        # setup our bounds
        base = 0
        limit = 0

        # find a seg and set the bounds
        if not _globals._mem.is_seg_00_full:
            base = 0
            limit = 255
            _globals._mem.is_seg_00_full = True

        elif not _globals._mem.is_seg_01_full:
            base = 256
            limit = 511
            _globals._mem.is_seg_01_full = True
        
        elif not _globals._mem.is_seg_02_full:
            base = 512
            limit = 767
            _globals._mem.is_seg_02_full = True

        else:
            # Throw an error for now, we are out of memory!!
            # This will becoming a routing to load onto the disk
            return [1, base, limit, 'disk']
        
        # load into memory
        memory_index = base
        for op_code in code:
            _globals._mem[memory_index] = op_code.upper()
            memory_index += 1
           

        return [0, base, limit, 'memory']

    def wipeSeg00(self):
        [ _globals._mem.append('00') for i in range(0,255) ]
    
    def wipeSeg01(self):
        [ _globals._mem.append('00') for i in range(256,511) ]

    def wipeSeg02(self):
        [ _globals._mem.append('00') for i in range(512,767) ]