class LoadStoreBuffer():
    def __init__(self, size):
        self.buffer = []
        self.size = size

    def isAvailable(self):
        return len(self.buffer) != self.size

    def append(self, data, rs):
        if self.isAvailable():
            self.buffer.append([data, rs])
        print(f"Buffer is full. Can't append [{data, rs}].")

