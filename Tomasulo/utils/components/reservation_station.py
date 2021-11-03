class ActiveReservationStation():
    def __init__(self, instruction, args):
        self.instruction = instruction
        self.args = args


    def isExecutable(self):
        """
        Check if the instruction is executable, 
        i.e. all the arguments are available.
        """
        for arg in self.args:
            if type(arg) == str:
                return False
        return True


    def updateDependency(self, rs_name):
        """
        Check if the instruction inside this RS depends on the
        provided rs_name. If it does, update it with the value 
        and return True. Otherwise, return False.
        The value is 1 as an abstraction.
        """
        for i in range(len(self.args)):
            if self.args[i] == rs_name:
                self.args[i] = 1
                return True
        return False

    def print(self):
        self.instruction.print()
        print(f"    Args: {self.args}")


class ReservationStations():
    def __init__(self, size, rs_type):
        self.stations = {}
        for i in range(1, size + 1):
            self.stations[rs_type + str(i)] = None


    def allocate(self, instruction, args):
        """
        Get an instruction that must wait for a busy register and
        store at the reservation station (RS). If the RS is full, 
        return None. Otherwise, return the RS name.
        """
        for key in self.stations.keys():
            if self.stations[key] == None:
                self.stations[key] = ActiveReservationStation(instruction, args)
                return key
        return None


    def free(self, rs_name):
        """
        Free the rs provided by clearing it.
        """
        self.stations[rs_name] = None


    def updateDependencies(self, rs_name):
        """
        Get a reservation station that just finished its execution and
        updates all other reservation stations that depended on it.
        Also, returns a list containing all of the RS which are free of
        dependencies.
        """
        executable_RSs = []
        for key in self.stations.keys():
            if self.stations[key] != None:
                updated = self.stations[key].updateDependency(rs_name)
                # Check if there is no other dependency for this RS
                if updated and self.stations[key].isExecutable():
                    executable_RSs.append(key)
        return executable_RSs

    def print(self):
        for name, station in self.stations.items():
            print(f"Station {name}:")
            if station != None:
                station.print()
