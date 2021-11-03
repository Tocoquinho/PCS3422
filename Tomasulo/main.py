from utils.instruction import Instruction
from utils.Tomasulo import TomasuloAlgorithm
from utils.event import Event, EventQueue

def eventEngine(event_queue):
    size_adder = 3
    size_multiplier = 2 

    # Instantiate Tomasulo's Algorithm object
    tomasulo = TomasuloAlgorithm(size_adder, size_multiplier)

    # Start event engine
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
    file_name = "instructions.txt"


    ###############################
    # Generate the event queue
    event_queue = EventQueue()

    # Read instruction file to get the events
    with open(file_name) as file:
        for i, instruction in enumerate(file):
            event = Event("Issued", i + 1, Instruction(instruction, i + 1))
            event_queue.append(event)
        
    # Run the Event Engine
    eventEngine(event_queue)


if __name__ == "__main__":
    main()
