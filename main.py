from cattle import Cattle
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

CHART_VERSIONS_EVOLUTION = 0
AVERAGE = 1
CHART_FREQUENCY_NEW_VERSION = 2
CHART_RANDOM = 3


CONFIG = CHART_RANDOM
TOPOLOGY = SIMPLE_TOPOLOGY
NB_NODES = 100
AVG_NB_NEIGHBOURS = 8
FREQ = 500


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

    if CONFIG == CHART_VERSIONS_EVOLUTION:
        if TOPOLOGY == SIMPLE_TOPOLOGY:
            cattle = create_cattle()
        elif TOPOLOGY == BROKEN_TOPOLOGY:
            cattle = broken_topology()
        else:
            cattle = random_topology(NB_NODES, AVG_NB_NEIGHBOURS)
        counter = 0
        next_update = counter + FREQ
        versions = []
        time_all_versions_equal = 0
        time = 0
        while True:
            try:
                counter += 1
                if counter == next_update:
                    [updated_node] = sample(cattle.connected_nodes, 1)
                    updated_node.n += 1
                    logging.info(f"main: update node {updated_node.name} to version {updated_node.n}")
                    logging.debug(f"main: update node {updated_node.name} to version {updated_node.n}")
                    next_update = counter + FREQ
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
                # time.sleep(0.1)
            except KeyboardInterrupt:
                print(f"All versions equal {100*time_all_versions_equal/time}% of the time")
                with open(FILE_NAME, 'w') as file:
                    json.dump(versions, file)
                f, ax = plt.subplots(1)
                for node in cattle.nodes:
                    ax.plot(list(range(len(versions))), [ver[node.name] for ver in versions], label=node.name)
                ax.set_ylim(ymin=0)
                plt.legend()
                plt.show()
                break
    elif CONFIG == AVERAGE:
        number_of_tries = 100
        cumulated_time = 0
        cumulated_code_sendings = 0
        failed = 0
        for i in range(number_of_tries):
            print(i)
            f = False
            with open('network.log', 'w'):
                pass
            if TOPOLOGY == SIMPLE_TOPOLOGY:
                model = create_cattle()
            elif TOPOLOGY == BROKEN_TOPOLOGY:
                model = broken_topology()
            else:
                model = random_topology(NB_NODES, AVG_NB_NEIGHBOURS)
            f = False
            for j in range(4):
                f = False
                cattle = copy.deepcopy(model)
                counter = 0
                while abs(cattle.coverage - 1) > 10e-4:
                    counter += 1
                    if counter == 1000:
                        f = True
                        break
                    cattle.tick()
                if f:
                    break
                cumulated_time += counter
                cumulated_code_sendings += cattle.get_number_of_code_sendings()

        print(f"\n\n\nAverage time to propagate new version: {cumulated_time/number_of_tries}\n"
              f"Average number of code sendings to propagate new version: {cumulated_code_sendings/number_of_tries}\n"
              f"Percentage of times failed: {failed/number_of_tries}")
    elif CONFIG == CHART_FREQUENCY_NEW_VERSION:
        frequencies, times_equal_versions = [], []
        for frequency in range(100, 1100, 100):
            print(frequency)
            s = 0
            for i in range(1000):
                with open('network.log', 'w'):
                    pass
                if TOPOLOGY == SIMPLE_TOPOLOGY:
                    cattle = create_cattle()
                elif TOPOLOGY == BROKEN_TOPOLOGY:
                    cattle = broken_topology()
                else:
                    cattle = random_topology(NB_NODES, AVG_NB_NEIGHBOURS)
                counter = 0
                next_update = counter + frequency
                time_all_versions_equal = 0
                time = 0
                while True:
                    counter += 1
                    if counter == next_update:
                        [updated_node] = sample(cattle.connected_nodes, 1)
                        updated_node.n += 1
                        if updated_node.n == 30:
                            break
                        logging.info(f"main: update node {updated_node.name} to version {updated_node.n}")
                        logging.debug(f"main: update node {updated_node.name} to version {updated_node.n}")
                        next_update = counter + frequency
                        logging.info(f"main: next update will occur at t={next_update}")
                        logging.debug(f"main: next update will occur at t={next_update}")
                    cattle.tick()
                    time += 1
                    if len(set(cattle.get_versions().values())) == 1:
                        time_all_versions_equal += 1
                s += time_all_versions_equal/time
            frequencies.append(frequency)
            times_equal_versions.append(100*s/1000)
        plt.plot(frequencies, times_equal_versions)
        plt.show()
    elif CONFIG == CHART_RANDOM:
        failures = []
        for k in range(3, 21, 2):
            print(k)
            number_of_tries = 10
            failed = 0
            for i in range(number_of_tries):
                with open('network.log', 'w'):
                    pass
                model = random_topology(NB_NODES, k)
                f = False
                for j in range(10):
                    f = False
                    cattle = model.copy()
                    counter = 0
                    while abs(cattle.coverage - 1) > 10e-4:
                        counter += 1
                        if counter == 1000:
                            f = True
                            break
                        cattle.tick()
                    if f:
                        break
                if f:
                    failed += 1
            failures.append(failed / 10)
        plt.plot(list(range(3, 21, 2)), failures)
        plt.show()
    else:
        print("ERROR: Unknown config!")
