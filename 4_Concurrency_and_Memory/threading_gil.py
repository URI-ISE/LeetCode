import threading

class Foo:
    def __init__(self):
        # Gates starts locked
        self.gate1 = threading.Lock()
        self.gate2 = threading.Lock()
        self.gate1.acquire()
        self.gate2.acquire()

    def first(self, printFirst):
        printFirst()
        # Unlock the first gate, allowing second() to proceed
        self.gate1.release()

    def second(self, printSecond):
        # Wait (Sleep) until gate1 is open
        with self.gate1: 
            printSecond()
            # Unlock the second gate
            self.gate2.release()

    def third(self, printThird):
        # Wait (Sleep) until gate2 is open
        with self.gate2:
            printThird()