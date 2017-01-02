from pybbn.graph.edge import Edge
from pybbn.graph.node import Node
from pybbn.graph.graph import Graph

n1 = Node(0)
n2 = Node(1)
n3 = Node(2)
e1 = Edge(n1, n2)
e2 = Edge(n2, n3)

g = Graph()
g.add_node(n1)
g.add_node(n2)
g.add_edge(e1)
g.add_edge(e2)

for node in g.get_nodes():
    print(node.key)

for edge in g.get_edges():
    print(edge.key)

for neighbor in g.get_neighbors(1):
    print(neighbor.uid)

