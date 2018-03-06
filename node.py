import random
from cattle import Cattle

class Node:
    def __init__(self, neighbours, I, n, code):
        self.neighbours = neighbours
        self.I = I
        self.n = n
        self.code = code
        self.tau = random.randint(I//2, I)
        self.c = 0
        self.t = 0
        self.inconsistent = False
        self.buffer = set()

    def broadcast(self, broadcast_code):
        if broadcast_code:
            code_to_broadcast = self.code
        else:
            code_to_broadcast = None
        for neighbour in self.neighbours:
            neighbour.receive(self.n, code_to_broadcast)

    def receive(self, n, code):
        self.buffer.add((n, code))

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def remove_neighbour(self, neighbour):
        self.neighbours.remove(neighbour)

    def update(self, n, code):
        self.n = n
        self.code = code

    def tick(self):
        for message in self.buffer:
            if message[0] == self.n:
                self.c += 1
            elif message[0] < self.n:
                self.broadcast(True)
                self.inconsistent = True
            elif message[0] > self.n and message[1] is None:
                self.broadcast(False)
                self.inconsistent = True
            else:
                self.update(*message)
                self.inconsistent = True
        if self.t == self.tau and self.c < self.k:
            self.broadcast(False)
        if self.t == self.I:
            if not self.inconsistent:
                self.I = min(Cattle.Imax, 2*self.I)
            else:
                self.I = Cattle.Imin
                self.reinit()

    def reinit(self):
        self.tau = random.randint(self.I // 2, self.I)
        self.c = 0
        self.t = 0
        self.inconsistent = False
        self.buffer = set()


