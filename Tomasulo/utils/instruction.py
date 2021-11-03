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
        
        # Execution information
        self.execution_time = None
        self.rs_name = None

        self.setInstructionParameters()


    def setInstructionParameters(self):
        """
        Transform the string instruction into the correct operation and
        determine its parameters (FP registers, address registers, etc)
        """
        instruction_types = {
            # logical-arithmetic
            'add'   : 'logical-arithmetic',
            'sub'   : 'logical-arithmetic',
            'xor'   : 'logical-arithmetic',
            'or'    : 'logical-arithmetic',
            'and'   : 'logical-arithmetic',
            'sll'   : 'logical-arithmetic',
            'srl'   : 'logical-arithmetic',
            'sra'   : 'logical-arithmetic',
            'slt'   : 'logical-arithmetic',
            'sltu'  : 'logical-arithmetic',

            # logical-arithmetic-imm
            'addi'  : 'logical-arithmetic-imm',
            'subi'  : 'logical-arithmetic-imm',
            'xori'  : 'logical-arithmetic-imm',
            'ori'   : 'logical-arithmetic-imm',
            'andi'  : 'logical-arithmetic-imm',
            'slli'  : 'logical-arithmetic-imm',
            'srli'  : 'logical-arithmetic-imm',
            'srai'  : 'logical-arithmetic-imm',
            'slti'  : 'logical-arithmetic-imm',
            'sltiu' : 'logical-arithmetic-imm',
    
            # u-imm
            'auipc' : 'au-imm',
            'lui'   : 'lu-imm',

            # load
            'lb'    : 'load',
            'lh'    : 'load',
            'lw'    : 'load',
            'lbu'   : 'load',
            'lhu'   : 'load',

            # store
            'sb'    : 'store',
            'sh'    : 'store',
            'sw'    : 'store',

            # branch-jump
            'beq'   : 'branch-jump',
            'bne'   : 'branch-jump',
            'blt'   : 'branch-jump',
            'bge'   : 'branch-jump',
            'bltu'  : 'branch-jump',
            'bgeu'  : 'branch-jump', 
            'jalrm' : 'branch-jump',
    
            # jump-imm
            'jal'   : 'jump-imm',

            #mul-div
            'mul'   : 'mul-div',
            'mulh'  : 'mul-div', 
            'mulhsu': 'mul-div',
            'mulhu' : 'mul-div',
            'div'   : 'mul-div',
            'divu'  : 'mul-div',
            'rem'   : 'mul-div',
            'remu'  : 'mul-div'
        }

        instruction_str = self.instruction.lower()

        # If the instruction presents the preamble
        if len(instruction_str) > 29:
            instruction_str = self.instruction[29:]
        
        # Split instruction name from its arguments in a list
        instruction_parts = instruction_str.split()
        # Split the operands in a list
        instruction_operation = instruction_parts[0]
        instruction_operands = instruction_parts[1].replace(', ', '').split(',')

        self.instruction_type = instruction_types[instruction_operation]
        self.input_registers = self.get_input_registers(instruction_types[instruction_operation], instruction_operands)
        self.output_register = self.get_output_registers(instruction_types[instruction_operation], instruction_operands)
        self.execution_time = self.get_execution_time(instruction_types[instruction_operation])

    
    def get_input_registers(self, instruction_type, operands):
        if instruction_type   == 'logical-arithmetic'       : return [operands[1], operands[2]]

        elif instruction_type == 'logical-arithmetic-imm'   : return [operands[1]]

        elif instruction_type == 'au-imm'                   : return []

        elif instruction_type == 'lu-imm'                   : return []

        elif instruction_type == 'load'                     : return [operands[1].split('(')[1].replace(')','')]

        elif instruction_type == 'store'                    : return [operands[0],operands[1].split('(')[1].replace(')','')]

        elif instruction_type == 'branch-jump'              : return [operands[0],operands[1]]

        elif instruction_type == 'jump-imm'                 : return []

        elif instruction_type == 'mul-div'                  : return [operands[1], operands[2]]

    def get_output_registers(self, instruction_type, operands):
        if instruction_type == 'store'          : return None
        elif instruction_type == 'branch-jump'  : return None
        elif instruction_type == 'jump-imm'     : return None
        else                                    : return operands[0]

    def get_execution_time(self, instruction_type):
        if instruction_type   == 'logical-arithmetic'       : return 1

        elif instruction_type == 'logical-arithmetic-imm'   : return 1

        elif instruction_type == 'au-imm'                   : return 4

        elif instruction_type == 'lu-imm'                   : return 4

        elif instruction_type == 'load'                     : return 8

        elif instruction_type == 'store'                    : return 2

        elif instruction_type == 'branch-jump'              : return 1

        elif instruction_type == 'jump-imm'                 : return 1

        elif instruction_type == 'mul-div'                  : return 10

    def print(self):
        instruction_txt = self.instruction.strip('\n')
        print(f"    Instruction: {instruction_txt}")
        print(f"    Steps:\n        {self.steps}")
