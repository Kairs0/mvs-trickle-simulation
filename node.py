import random
import logging

BROADCAST = False

logging.basicConfig(filename='network.log', level=logging.INFO)


class Node:
    id_counter = 0

    def __init__(self, name, n, i, k, imin, imax):
        self.id = Node.id_counter
        Node.id_counter += 1

        self.name = name
        self.n = n
        self.i = i
        self.k = k
        self.imin = imin
        self.imax = imax
        self.neighbours = set()

        self.tau = random.randint(i//2, i)
        self.c = 0
        self.t = 0
        self.inconsistent = False
        self.buffer = set()

        self.number_of_sent_messages = 0

    def broadcast(self, broadcast_code):
        if broadcast_code:
            logging.info(f"Node {self.name}: broadcast number {self.n} to neighbours, with code")
            logging.debug(f"Node {self.name}: broadcast number {self.n} to neighbours, with code")
        else:
            logging.info(f"Node {self.name}: broadcast number {self.n} to neighbours")
            logging.debug(f"Node {self.name}: broadcast number {self.n} to neighbours")
        self.number_of_sent_messages += 1
        for neighbour in self.neighbours:
            neighbour.receive(self.n, broadcast_code)

    def receive(self, n, code):
        logging.info(f"Node {self.name} added number {n} into buffer")
        logging.debug(f"Node {self.name} added number {n} into buffer")
        self.buffer.add((n, code))

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def remove_neighbour(self, neighbour):
        self.neighbours.remove(neighbour)

    def update(self, n):
        logging.debug(f"Node {self.name}: Code updated from version {self.n} to version {n}")
        logging.info(f"Node {self.name}: Code updated from version {self.n} to version {n}")
        self.n = n

    def tick(self):
        self.t += 1
        for message in self.buffer:
            if message[1]:
                logging.info(f"Node {self.name} received number {message[0]} with code")
                logging.debug(f"Node {self.name} received number {message[0]} with code")
            else:
                logging.info(f"Node {self.name} received number {message[0]}")
                logging.debug(f"Node {self.name} received number {message[0]}")
            if message[0] == self.n:
                self.c += 1
            elif message[0] < self.n:
                self.broadcast(True)
                self.inconsistent = True
            elif message[0] > self.n and not message[1]:
                self.broadcast(False)
                self.inconsistent = True
            else:
                self.update(message[0])
                self.inconsistent = True
        self.buffer = set()
        if self.t == self.tau and self.c < self.k:
            self.broadcast(BROADCAST)
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

    def copy(self):
        return Node(self.name, self.n, self.i, self.k, self.imin, self.imax)
