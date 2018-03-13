from cattle import Cattle

cattle = Cattle()

A = cattle.new_node("A", 2)
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

cattle.start(0.2)
