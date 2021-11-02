class Register():
    def __init__(self, data = None, rs = None):
        self.data = data
        self.rs = rs

    def isBusy():
        """
        Return a boolean indicating whether or not the register is busy.
        It is busy if the reservation station is not empty.
        """
        return self.rs != None
    

class FPRegisters():
    def __init__(self, size):
        self.registers = {}
        for i in range(1, size + 1):
            self.registers['R' + str(i)] = Register()

    
    def updateDependencies(self, rs_name, data):
        """
        Get a reservation station that just finished its execution and
        updates all registers that depended on it.
        """
        for key in self.registers.keys():
            if self.registers[key].rs == rs_name:
                self.registers[key].data = data
                self.registers[key].rs = None
