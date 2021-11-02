class ActiveReservationStation():
    def __init__(self, instruction, args):
        self.instruction = instruction
        self.args = args


    def isExecutable():
        """
        Check if the instruction is executable, 
        i.e. all the arguments are available.
        """
        for arg in args:
            if type(arg) == str:
                return False
        return True


    def updateDependency(self, rs_name, data):
        """
        Checks if the instruction inside this RS depends on the
        provided rs_name. If it does, update it with the value
        """
        for i in range(len(args)):
            if args[i] == rs_name:
                args[i] = data
    

    def calculateResult():
        """
        Calculates the result of the instruction.
        """
        operation = self.instruction.instruction_type
        if operation == '+':
            return args[0] + args[1]

        if operation == '-':
            return args[0] - args[1]

        if operation == '*':
            return args[0] * args[1]

        if operation == '/':
            try:
                return args[0] / args[1]
            except:
                return None
        else:
            return None


class ReservationStations():
    def __init__(self, size, rs_type):
        self.stations = {}
        for i in range(1, size + 1):
            stations[rs_type + str(i)] = None


    def append(self, instruction_type, args, instruction):
        """
        Get an instruction that must wait for a busy register and
        store at the reservation station (RS). If the RS is full, 
        return None. Otherwise, return the RS name.
        """
        for key in self.station.keys():
            if self.station[key] == None:
                self.station[key] = ActiveReservationStation(instruction, args)
                return key
        return None


    def free(self, rs_name):
        """
        Free the rs provided by clearing it.
        """
        self.stations[rs_name] = None


    def updateDependencies(self, rs_name, data):
        """
        Get a reservation station that just finished its execution and
        updates all other reservation stations that depended on it.
        Also, returns a list containing all of the RS which are free of
        dependencies.
        """
        executable_RSs = []
        for key in self.station.keys():
            if self.station[key] == None:
                self.station[key].updateDependency(rs_name, data)
                # Check if there is no other dependency for this RS
                if self.station[key].isExecutable():
                    executable_RSs.append(key)
        return executable_RSs

