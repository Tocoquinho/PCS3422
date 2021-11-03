# Events:
    # Issued: t = 0
    # Finished: t = start + execution_time

class Event:
    def __init__(self, event_type, time, instruction = None):
        self.event_type = event_type
        self.time = time
        self.instruction = instruction


    def print(self):
        instruction_str = ""
        if self.instruction != None:
            instruction_str = ": " + self.instruction.instruction
        
        print(f"    {self.time:03} - {self.event_type}{instruction_str}", end="")


class EventQueue:
    def __init__(self):
        self.queue = []


    def isEmpty(self):
        return len(self.queue) == 0


    def addEvent(self, new_event):
        index = len(self.queue)
        for i, event in enumerate(self.queue):
            if event.time > new_event.time:
                index = i 
                break
        self.queue.insert(index, new_event)


    def getNextEvent(self):
        return self.queue.pop(0)


    def print(self):
        print("Event Queue: ")
        for event in self.queue:
            event.print()
