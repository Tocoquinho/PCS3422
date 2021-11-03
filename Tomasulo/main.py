from utils.instruction import Instruction
from utils.Tomasulo import TomasuloAlgorithm
from utils.event import Event, EventQueue

def eventEngine(event_queue, tomasulo):
    # Start event engine
    print("\n------------------------------------------")
    print("Type enter to start the simulation: ")
    while not event_queue.isEmpty():
        # Get simulation step command
        if(input() != ""):
            continue
        
        event_queue.print()
        tomasulo.print()
        print("------------------------------------------")

        # Send next event to the system
        event = event_queue.getNextEvent()
        new_events = tomasulo.receiveEvent(event)

        # Tranform new events in a list
        if type(new_events) != list:
            new_events = [new_events]

        # If there is a new event, add it to the queue
        for new_event in new_events:
            if new_event != None:
                event_queue.addEvent(new_event)




def main():
    ###############################
    # Parameters

    # Default Values
    default_file_name = "instructions.txt"
    default_size_adder = 3
    default_size_multiplier = 2
    default_size_load = 3
    default_size_fp_register = 4
    default_size_ad_register = 4

    # File name
    print("Type the instruction file name")
    file_name = input(f"[Empty for deafult option: '{default_file_name}']")
    if(file_name == ''):
        file_name = default_file_name

    # Reservation Station sizes
    print("\nType the Number of Adder Reservation Stations")
    size_adder = input(f"[Empty for deafult option: {default_size_adder}]")
    if(size_adder == ''):
        size_adder = default_size_adder
    else:
        size_adder = int(size_adder)

    print("\nType the Number of Multiplier Reservation Stations")
    size_multiplier = input(f"[Empty for deafult option: {default_size_multiplier}]")
    if(size_multiplier == ''):
        size_multiplier = default_size_multiplier
    else:
        size_multiplier = int(size_multiplier)
        
    print("\nType the Number of Loader Reservation Stations")
    size_load = input(f"[Empty for deafult option: {default_size_load}]")
    if(size_load == ''):
        size_load = default_size_load
    else:
        size_load = int(size_load)

    print("\nType the Number of Floating Point Registers")
    size_fp_registers = input(f"[Empty for deafult option: {default_size_fp_registers}]")
    if(size_fp_registers == ''):
        size_fp_registers = default_size_fp_registers
    else:
        size_fp_registers = int(size_fp_registers)

    print("\nType the Number of Address Registers")
    size_ad_registers = input(f"[Empty for deafult option: {default_size_ad_registers}]")
    if(size_ad_registers == ''):
        size_ad_registers = default_size_ad_registers
    else:
        size_ad_registers = int(size_ad_registers)

    ###############################
    # Generate the event queue
    event_queue = EventQueue()
    instruction_list = []

    # Read instruction file to get the events
    with open(file_name) as file:
        for i, instruction in enumerate(file):
            event = Event("Issued", i + 1, Instruction(instruction, i + 1))
            event_queue.addEvent(event)
            instruction_list.append(event.instruction)
        
    # Instantiate Tomasulo's Algorithm object
    tomasulo = TomasuloAlgorithm(size_adder, size_multiplier, size_load, size_fp_registers, size_ad_registers)

    # Run the Event Engine
    eventEngine(event_queue, tomasulo)

    print("Processing ended.\nFinal Results: ")
    for instruction in instruction_list:
        instruction.print()
        print()


if __name__ == "__main__":
    main()
