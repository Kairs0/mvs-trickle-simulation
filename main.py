from cattle import Cattle
from random import randint, sample
import time

def create_cattle():
    cattle = Cattle()

    A = cattle.new_node("A", 2, connected=True)
    B = cattle.new_node("B", 1)
    C = cattle.new_node("C", 1)
    D = cattle.new_node("D", 1)
    E = cattle.new_node("E", 1)


    A.add_neighbour(B)
    A.add_neighbour(D)

    B.add_neighbour(C)
    B.add_neighbour(E)

    C.add_neighbour(E)

    D.add_neighbour(E)

    E.add_neighbour(A)
    E.add_neighbour(B)

    return cattle


def broken_topology():
    # Create a cyclic cattle preventing 100% update coverage
    cattle = Cattle()

    A = cattle.new_node("A", 1, connected=True)
    B = cattle.new_node("B", 1)
    C = cattle.new_node("C", 1)
    D = cattle.new_node("D", 1)
    E = cattle.new_node("E", 1)

    A.add_neighbour(B)
    A.add_neighbour(C)
    A.add_neighbour(D)
    B.add_neighbour(E)
    C.add_neighbour(E)
    D.add_neighbour(E)
    E.add_neighbour(A)

    return cattle


if __name__ == "__main__":
    cattle = broken_topology()
    counter = 0
    next_update = counter + randint(50, 100)

    while True:
        counter += 1
        if counter == next_update:
            [updated_node] = sample(cattle.connected_nodes, 1)
            updated_node.n += 1
            print(f"main: update node {updated_node.name} to version {updated_node.n}")
            next_update = counter + randint(500, 600)
            print(f"main: next update will occur at t={next_update}")

        cattle.tick()
        time.sleep(0.05)


