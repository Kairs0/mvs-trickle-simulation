from cattle import Cattle

cattle = Cattle()

cattle.new_node("A", 2)
cattle.new_node("B", 1)
cattle.new_node("C", 1)
cattle.new_node("D", 1)
cattle.new_node("E", 1)

cattle.get_node_by_name("A").add_neighbour(cattle.get_node_by_name("B"))
cattle.get_node_by_name("A").add_neighbour(cattle.get_node_by_name("D"))

cattle.get_node_by_name("B").add_neighbour(cattle.get_node_by_name("C"))
cattle.get_node_by_name("B").add_neighbour(cattle.get_node_by_name("E"))

cattle.get_node_by_name("C").add_neighbour(cattle.get_node_by_name("E"))

cattle.get_node_by_name("D").add_neighbour(cattle.get_node_by_name("E"))

cattle.get_node_by_name("E").add_neighbour(cattle.get_node_by_name("A"))
cattle.get_node_by_name("E").add_neighbour(cattle.get_node_by_name("B"))
