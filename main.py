from cattle import Cattle

cattle = Cattle()

A = cattle.new_node("A", 2)
B = cattle.new_node("B", 1)
C = cattle.new_node("C", 1)
D = cattle.new_node("D", 1)
E = cattle.new_node("E", 1)

cattle.get_node_by_name("A").add_neighbour(B)
cattle.get_node_by_name("A").add_neighbour(D)

cattle.get_node_by_name("B").add_neighbour(C)
cattle.get_node_by_name("B").add_neighbour(E)

cattle.get_node_by_name("C").add_neighbour(E)

cattle.get_node_by_name("D").add_neighbour(E)

cattle.get_node_by_name("E").add_neighbour(A)
cattle.get_node_by_name("E").add_neighbour(B)

cattle.start(0.2)
