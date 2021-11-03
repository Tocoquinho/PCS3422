class SingleRegister():
    def __init__(self, rs = None):
        self.rs = rs

    def isBusy(self, rs_name):
        """
        Return a boolean indicating whether or not the register is busy.
        It is busy if the reservation station is not empty.
        """
        return self.rs != None and self.rs != rs_name
    
    def print(self):
        print(f"    rs: {self.rs}")
    

class Registers():
    def __init__(self, type, size):
        self.registers = {}
        for i in range(0, size):
            self.registers[type + str(i)] = SingleRegister()

    
    def updateDependencies(self, rs_name):
        """
        Get a reservation station that just finished its execution and
        updates all registers that depended on it.
        """
        for key in self.registers.keys():
            if self.registers[key].rs == rs_name:
                self.registers[key].rs = None

    def print(self):
        for name, register in self.registers.items():
            print(f"Register {name}")
            register.print()
            