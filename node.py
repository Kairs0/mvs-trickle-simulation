import random


class Node:
    id_counter = 0

    def __init__(self, name, n, i, k, imin, imax, neighbours=set()):
        self.id = Node.id_counter
        Node.id_counter += 1

        self.name = name
        self.n = n
        self.i = i
        self.k = k
        self.imin = imin
        self.imax = imax
        self.neighbours = neighbours

        self.tau = random.randint(i//2, i)
        self.c = 0
        self.t = 0
        self.inconsistent = False
        self.buffer = set()

    def broadcast(self, broadcast_code):
        if broadcast_code:
            print(f"Broadcast number {self.n} from node {self.name} to neighbours, with code")
        else:
            print(f"Broadcast number {self.n} from node {self.name} to neighbours")
        for neighbour in self.neighbours:
            neighbour.receive(self.n, broadcast_code)

    def receive(self, n, code):
        print(f"Node {self.name} received number {n}")
        self.buffer.add((n, code))

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def remove_neighbour(self, neighbour):
        self.neighbours.remove(neighbour)

    def update(self, n):
        self.n = n
        print(f"Node {self.name}: Code updated from version {n-1} to version {n}")

    def tick(self):
        self.t += 1
        for message in self.buffer:
            print(f"Buffer: {self.buffer}")
            if message[1]:
                print(f"Received number {message[0]} with code")
            else:
                print(f"Received number {message[0]}")
            if message[0] == self.n:
                self.c += 1
            elif message[0] < self.n:
                self.broadcast(True)
                self.inconsistent = True
            elif message[0] > self.n and not message[1]:
                self.broadcast(False)
                self.inconsistent = True
            else:
                self.update(*message)
                self.inconsistent = True
        self.buffer = set()
        if self.t == self.tau and self.c < self.k:
            self.broadcast(False)
        if self.t == self.i:
            if not self.inconsistent:
                self.i = min(self.imax, 2*self.i)
            else:
                self.i = self.imin
            self.reinit()

    def reinit(self):
        self.tau = random.randint(self.i // 2, self.i)
        self.c = 0
        self.t = 0
        self.inconsistent = False
        self.buffer = set()
