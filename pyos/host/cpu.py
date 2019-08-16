from pyos.globals import _globals

class CPU:
    def __init__(self):
        self.pc = 0
        self.acc = 0
        self.x_reg = 0
        self.y_reg = 0
        self.z_flag = 0
        self.is_executing = False
    
    def cycle(self):
        _globals._kernal.krnTrace('CPU cycle');
        # TODO: Accumulate CPU usage and profiling statistics here.
        # Do the real work here. Be sure to set this.isExecuting appropriately.
