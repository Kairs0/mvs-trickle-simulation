from cattle import Cattle
import node
from random import randint, sample, random
import json
import matplotlib.pyplot as plt
import time
import copy

import logging

logging.basicConfig(filename='network.log', level=logging.INFO)


DUMPING_FREQ = 25
FILE_NAME = "trace.txt"

SIMPLE_TOPOLOGY = 0
BROKEN_TOPOLOGY = 1
RANDOM_TOPOLOGY = 2

CHART_VERSIONS_EVOLUTION = 3
AVERAGE = 4
CHART_RANDOM = 5

BASIC = 6
VARIANT = 7

# Change these variables here
CONFIG = CHART_RANDOM

TOPOLOGY = BROKEN_TOPOLOGY

FREQ_NEW_VERSION = 100

NB_NODES = 100

AVG_NB_NEIGHBOURS = 2

ALGORITHM_VERSION = VARIANT
# End of the section you should change


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

    A = cattle.new_node("A", 2, connected=True)
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

def random_topology(n, avg_nb_neighbours):
    cattle = Cattle()

    cattle.new_node("0", 2, connected=True)
    for i in range(1, n):
        cattle.new_node(str(i), 1)
    for i in range(n):
        node = cattle.get_node_by_name(str(i))
        for j in range(n):
            if i != j and n*random() < avg_nb_neighbours:
                node.add_neighbour(cattle.get_node_by_name(str(j)))
                #print(f"{i} has {j} as neighbour")

    return cattle


if __name__ == "__main__":
    # empty log file
    with open('network.log', 'w'):
        pass
    node.BROADCAST = ALGORITHM_VERSION == VARIANT
    if CONFIG == CHART_VERSIONS_EVOLUTION:
        if TOPOLOGY == SIMPLE_TOPOLOGY:
            cattle = create_cattle()
        elif TOPOLOGY == BROKEN_TOPOLOGY:
            cattle = broken_topology()
        else:
            cattle = random_topology(NB_NODES, AVG_NB_NEIGHBOURS)
        counter = 0
        next_update = counter + FREQ_NEW_VERSION
        versions = []
        time_all_versions_equal = 0
        time = 0
        while True:
            counter += 1
            if counter == next_update:
                [updated_node] = sample(cattle.connected_nodes, 1)
                updated_node.n += 1
                logging.info(f"main: update node {updated_node.name} to version {updated_node.n}")
                logging.debug(f"main: update node {updated_node.name} to version {updated_node.n}")
                next_update = counter + FREQ_NEW_VERSION
                logging.info(f"main: next update will occur at t={next_update}")
                logging.debug(f"main: next update will occur at t={next_update}")
            cattle.tick()
            time += 1
            if len(set(cattle.get_versions().values())) == 1:
                time_all_versions_equal += 1
            versions.append(cattle.get_versions())
            if counter % DUMPING_FREQ == 0:
                with open(FILE_NAME, 'w') as file:
                    json.dump(versions, file)
            if time == 5000:
                break
        print(f"All versions equal {100*time_all_versions_equal/time}% of the time")
        with open(FILE_NAME, 'w') as file:
            json.dump(versions, file)
        f, ax = plt.subplots(1)
        for node in cattle.nodes:
            ax.plot(list(range(len(versions))), [ver[node.name] for ver in versions], label=node.name)
        ax.set_ylim(ymin=0)
        plt.legend()
        plt.show()
        exit()
    elif CONFIG == AVERAGE:
        number_of_tries = 100
        cumulated_time = 0
        cumulated_code_sendings = 0
        failed = 0
        for i in range(number_of_tries):
            with open('network.log', 'w'):
                pass
            if TOPOLOGY == SIMPLE_TOPOLOGY:
                cattle = create_cattle()
            elif TOPOLOGY == BROKEN_TOPOLOGY:
                cattle = broken_topology()
            else:
                cattle = random_topology(NB_NODES, AVG_NB_NEIGHBOURS)
            f = False
            counter = 0
            last_coverage = 0
            while abs(cattle.coverage - 1) > 10e-4:
                if cattle.coverage != last_coverage:
                    last_coverage = cattle.coverage
                    counter = 0
                counter += 1
                if counter == 1000:
                    failed += 1
                    f = True
                    break
                cattle.tick()
            if not f:
                cumulated_time += counter
                cumulated_code_sendings += cattle.get_number_of_code_sendings()
        if failed != number_of_tries:
            print(f"\n\n\nAverage time to propagate new version: {cumulated_time/(number_of_tries-failed)}\n"
                  f"Average number of messages sent to propagate new version: {cumulated_code_sendings/(number_of_tries-failed)}\n"
                  f"Percentage of times failed: {failed/number_of_tries}")
        else:
            print("Percentage of times failed: 1.0")
    elif CONFIG == CHART_RANDOM:
        K = []
        failures = []
        for k in range(1, NB_NODES):
            K.append(k)
            print(k)
            number_of_tries = 50
            failed = 0
            for i in range(number_of_tries):
                with open('network.log', 'w'):
                    pass
                cattle = random_topology(NB_NODES, k)
                f = False
                counter = 0
                last_coverage = 0
                while abs(cattle.coverage - 1) > 10e-4:
                    if cattle.coverage != last_coverage:
                        last_coverage = cattle.coverage
                        counter = 0
                    counter += 1
                    if counter == 1000:
                        f = True
                        break
                    cattle.tick()
                if f:
                    failed += 1
            failures.append(failed / number_of_tries)
            if len(failures) >= 5 and failures[-1] == failures[-2] == failures[-3] == failures[-4] == failures[-5] == 0:
                break
        plt.plot(K, failures)
        plt.show()
    else:
        print("ERROR: Unknown config!")
