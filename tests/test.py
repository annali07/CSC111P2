import numpy as np
import networkx as nx
import time
import matplotlib.pyplot as plt

edge_list = [(1,2), (2,3), (3, 4), (1, 4)]

G = nx.Graph()
#G = nx.DiGraph()
#G = nx.MultiGraph()
#G = nx.from_edgelist(edge_list)
G.add_node(5)
G.add_node(6)
G.add_node(7)
#G.add_edge(1, 2)
#G.add_edge(2, 3, weight=0.9)
#G.add_edge("A", "B")
#G.add_edge("B", "B")
#print(nx.adjacency_matrix(G))

for i in range(0, 2):
   G.add_edge(i, 5)
   time.sleep(2)
   nx.draw_spring(G, with_labels=True)
    

plt.show()
