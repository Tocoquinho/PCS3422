from components.buffer import LoadStoreBuffer
from components.reservation_station import ActiveReservationStation, ReservationStations
from components.register import Register, FPRegisters
from event import Event, EventQueue
from instruction import Instruction

class TomasuloAlgorithm():
    def __init__(self, size_adder, size_multiplier, size_fp_registers = 4):
        self.fp_registers = FPRegisters(size_fp_registers)
        self.rs_adder = ReservationStations(size_adder, "Add")
        self.rs_multiplier = ReservationStations(size_multiplier, "Mul")
        self.clock = 0
        
    
    def receiveEvent(self, event):
        """
        Get an event and process it
        """
        self.clock += event.time
        event_type = event.event_type

        if event_type == "Issued":
            return self.eventIssued()
        
        elif event_type == "Finished":
            return self.eventFinished(event)


    def eventIssued(self, event):
        """
        Process the event typed as Issue, when an instruction arrives at the system
        """

        # Get the instruction information: type and input/output registers
        instruction_type = event.instruction.instruction_type
        input_registers = event.instruction.input_registers
        output_register = event.instruction.output_register

        # Try to send the instruction to its specific reservation station (RS)
        current_rs = None
        rs_name = None
        if instruction_type in ['+', '-']:
            current_rs = self.rs_adder
            rs_name = self.rs_adder.append(instruction, input_registers)

        elif instruction_type in ['*', '/']:
            current_rs = self.rs_multiplier
            rs_name = self.rs_multiplier.append(instruction, input_registers)

        else:
            # TODO: GO TO BUFFER
            pass

        # Check if the reservation station was available
        if rs_name == None:
            # TODO: WHAT HAPPENS IF RS NOT AVAILABLE??
            pass
        else:
            # Update the reservation station of the instruction
            event.instruction.rs_name = rs_name

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
                return self.startExecution(rs_name)
        return None


    def eventFinished(self, event):
        """
        Process the event typed as Finished, when the execution of an instruction finishes
        """
        
        # Detect the reservation station used
        current_rs = None
        rs_name = event.instruction.rs_name
        if rs_name[:-1] == "Add":
            current_rs = self.rs_adder
        else:
            current_rs = self.rs_multiplier

        # Update the calculated value into the output register/memory
        output_register = event.instruction.output_register
        result = current_rs[rs_name].calculateResult()
        self.fp_registers.registers[output_register] = result

        # Check if there is any other subscriber of that output
        self.findSubscribers(rs_name, result)

        # Update the "Finished" status of the instruction
        event.instruction.steps["Finished"] = self.clock


    def startExecution(self, rs_name):
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
        instruction.steps["Started"] = self.clock
        return Event("Finished", self.clock + instruction.execution_time, 
                     instruction)


    def findSubscribers(self, rs_name, data):
        """
        Look for instructions waiting for the output of that RS, 
        which has finished calculating the result. Update each of them.
        """

        new_events = []

        # Update subscribers in rs_adder and execute the possible ones
        for executable_rs in self.rs_adder.updateDependencies(rs_name, data):
            new_events.append(self.startExecution(executable_rs))

        # Update subscribers in rs_multiplier and execute the possible ones
        for executable_rs in self.rs_multiplier.updateDependencies(rs_name, data):
            new_events.append(self.startExecution(executable_rs))

        # Update subscribers in fp_registers and execute the possible ones
        self.fp_registers.updateDependencies(rs_name, data)

        # Update subscribers in the buffer and execute the possible ones
        # TODO
