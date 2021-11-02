class Instruction:
    def __init__(self, instruction, issue_time):
        self.instruction = instruction
        self.steps = {"Issued": issue_time,
                      "Started": None,
                      "Finished": None,
                      "Written": None
                      }

        # Instruction data
        self.instruction_type = None
        self.input_registers = []
        self.output_register = None
        self.setInstructionParameters()

        # Execution information
        self.execution_time = None
        self.rs_name = None


    def setInstructionParameters():
        """
        Transform the string instruction into the correct operation and
        determine its parameters (FP registers, address registers, etc)
        """
        # UPDATE THIS
        self.instruction_type = '+'
        self.input_registers = ["R1", "R2"]
        self.output_register = "R3"
        self.execution_time = 10

