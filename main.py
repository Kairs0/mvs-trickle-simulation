from cattle import Cattle
from random import randint, sample
import time

import logging

logging.basicConfig(filename='network.log', level=logging.INFO)

import json
import matplotlib.pyplot as plt

DUMPING_FREQ = 25
FILE_NAME = "trace.txt"


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
    # empty log file
    with open('network.log', 'w'):
        pass

    cattle = broken_topology()
    counter = 0
    next_update = counter + randint(50, 100)
    make_chart = False
    update = False
    #cattle = broken_topology()
    cattle = create_cattle()
    counter = 0
    next_update = -1
    if update:
        next_update = counter + randint(50, 100)

    versions = []

    while True:
        try:
            counter += 1
            if counter == next_update:
                [updated_node] = sample(cattle.connected_nodes, 1)
                updated_node.n += 1
                logging.info(f"main: update node {updated_node.name} to version {updated_node.n}")
                print(f"main: update node {updated_node.name} to version {updated_node.n}")
                next_update = counter + randint(50, 100)
                logging.info(f"main: next update will occur at t={next_update}")
                print(f"main: next update will occur at t={next_update}")

            cattle.tick()
            versions.append(cattle.get_versions())
            if counter % DUMPING_FREQ == 0:
                with open(FILE_NAME, 'w') as file:
                    json.dump(versions, file)
            time.sleep(0.1)
        except KeyboardInterrupt:
            if make_chart:
                with open(FILE_NAME, 'w') as file:
                    json.dump(versions, file)
                f, ax = plt.subplots(1)
                for node in cattle.nodes:
                    ax.plot(list(range(len(versions))), [ver[node.name] for ver in versions], label=node.name)
                ax.set_ylim(ymin=1)
                plt.legend()
                plt.show()
            break
