import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

edge_list = [(1,2), (2,3), (3, 4), (1, 4)]

G = nx.Graph()
G.add_nodes_from(range(1, 8))  # Add nodes 1-7
G.add_edges_from(edge_list)

pos = nx.spring_layout(G)

plt.ion()  # Turn on interactive mode

for i in range(0, 5):
    G.add_edge(i, 5)  # This will add edges (0,5) and then (1,5)

    plt.clf()  # Clear the current figure
    nx.draw(G, pos=pos, with_labels=True)   
    plt.pause(1)  # Pause for 2 seconds before continuing

plt.ioff()  # Turn off interactive mode
plt.show()  # Show the final plot

