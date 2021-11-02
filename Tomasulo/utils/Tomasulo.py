from components.reservation_station import ActiveReservationStation, ReservationStations
from components.register import SingleRegister, Registers
from event import Event, EventQueue
from instruction import Instruction
from utils import instruction

class TomasuloAlgorithm():
    def __init__(self, size_adder, size_multiplier, size_load, 
                 size_fp_registers = 4, size_ad_registers = 4):
        self.fp_registers = Registers('F', size_fp_registers)
        self.ad_registers = Registers('R', size_ad_registers)
        self.rs_adder = ReservationStations(size_adder, "Add")
        self.rs_multiplier = ReservationStations(size_multiplier, "Mul")
        self.rs_load = ReservationStations(size_load, "Load")
        self.clock = 0
        
    
    def receiveEvent(self, event):
        """
        Get an event and process it.
        """
        self.clock += event.time
        event_type = event.event_type

        if event_type == "Issued":
            return self.eventIssued()
        
        elif event_type == "Finished":
            return self.eventFinished(event)

        elif event_type == "Writen":
            return self.eventWritten(event)


    def eventIssued(self, event):
        """
        Process the event typed as Issued, when an instruction arrives at the system.
        """
        # Get the instruction information: type and input/output registers
        instruction_type = event.instruction.instruction_type
        input_registers = event.instruction.input_registers
        output_register = event.instruction.output_register

        # Try to send the instruction to its specific reservation station (RS)
        current_rs = None
        rs_name = None
        if instruction_type == "logical-arithmetic":
            current_rs = self.rs_adder
            rs_name = self.rs_adder.allocate(event.instruction, input_registers)

        elif instruction_type == "mul-div":
            current_rs = self.rs_multiplier
            rs_name = self.rs_multiplier.allocate(event.instruction, input_registers)

        elif instruction_type in ["load", "store"]:
            current_rs = self.rs_load
            rs_name = self.rs_load.allocate(event.instruction, input_registers)
            pass

        # Check if the reservation station was available
        if rs_name == None:
            # TODO: WHAT HAPPENS IF RS NOT AVAILABLE??
            pass
        else:
            # Update the reservation station of the instruction
            event.instruction.rs_name = rs_name

            # Update the reservation station of the output register
            self.fp_registers.registers[output_register].rs = rs_name

            # Check any input register not available (busy)
            for i, register in enumerate(current_rs[rs_name].args):
                if self.fp_registers.registers[register].isBusy():
                    # The instruction must wait for the register
                    current_rs[rs_name].args[i] = self.fp_registers.registers[register].rs
                else:
                    # Get the register value and make it busy
                    current_rs[rs_name].args[i] = self.fp_registers.registers[register].data
                    self.fp_registers.registers[register].rs = rs_name

            # Try to execute the instruction
            if current_rs[rs_name].isExecutable():
                return self.startExecution(rs_name, event.instruction)
        return None


    def eventFinished(self, event):
        """
        Process the event typed as Finished, when the execution of an instruction finishes.
        """
        # Reservation station used
        rs_name = event.instruction.rs_name
    
        # Check if there is any other RS which is a subscriber of that output
        # and start their execution if it is possible now
        new_events = self.findSubscribers(rs_name)

        # Update the "Finished" status of the instruction
        event.instruction.steps["Finished"] = self.clock

        new_events.append(Event("Written", self.clock + 1, event.instruction))

        return new_events


    def eventWritten(self, event):
        """
        Process the event typed as Written, when the result of an instruction goes to the register.
        """
        # Reservation station used
        rs_name = event.instruction.rs_name     
        # Update subscribers in fp_registers and execute the possible ones
        self.fp_registers.updateDependencies(rs_name)
        # # Update the "Writen" status of the instruction
        event.instruction.steps["Written"] = self.clock


    def startExecution(self, rs_name, instruction):
        """
        Start the execution of the instruction and clear the RS
        """
        # Clear the reservation station
        if rs_name[:-1] == "Add":
            current_rs = self.rs_adder
        else:
            current_rs = self.rs_multiplier
        current_rs.free(rs_name)
        
        # Start the execution
        instruction.steps["Started"] = self.clock + 1
        return Event("Finished", self.clock + 1 + instruction.execution_time, 
                     instruction)


    def findSubscribers(self, rs_name):
        """
        Look for instructions waiting for the output of that RS, 
        which has finished calculating the result. Update each of them.
        """
        new_events = []

        # Update subscribers in rs_adder and execute the possible ones
        for executable_rs in self.rs_adder.updateDependencies(rs_name):
            instruction = self.rs_adder.stations[executable_rs].instruction
            new_events.append(self.startExecution(executable_rs, instruction))

        # Update subscribers in rs_multiplier and execute the possible ones
        for executable_rs in self.rs_multiplier.updateDependencies(rs_name):
            instruction = self.rs_multiplier.stations[executable_rs].instruction
            new_events.append(self.startExecution(executable_rs))

        # Update subscribers in the buffer and execute the possible ones
        for executable_rs in self.rs_load.updateDependencies(rs_name):
            instruction = self.rs_load.stations[executable_rs].instruction
            new_events.append(self.startExecution(executable_rs))

        return new_events

    def print(self):
        print(f"Clock: {self.clock}")
        self.fp_registers.print()
        self.ad_registers.print()
        self.rs_adder.print()
        self.rs_multiplier.print()
        self.rs_load.print()