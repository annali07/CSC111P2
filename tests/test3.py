import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# edge_list = [(1, 2), (2, 3), (3, 4), (1, 4)]

G = nx.Graph()
G.add_nodes_from(range(1, 8))  # Add nodes 1-7
# G.add_edges_from(edge_list)

# Fix the positions
positions = nx.spring_layout(G)

plt.ion()  # Turn on interactive mode
colors = ['blue'] * nx.number_of_nodes(G)  # Initial color of all nodes

for i in range(1, 8):  # Assume we have 8 iterations for demonstration
    if i < 5:
        G.add_edge(i, i + 1)  # Add a new edge to the graph
    
    plt.clf()  # Clear the current figure

    # Change the color of the new node and its edges
    node_colors = ['red' if node in [i, i + 1] else 'blue' for node in G.nodes()]

    # Redraw the graph with fixed positions
    nx.draw(G, pos=positions, node_color=node_colors, with_labels=True)
    plt.title('Main Title Here', loc='center')
    plt.text(0.5, 1.05, f'The {i}th Day', 
         ha='center', va='bottom', transform=plt.gca().transAxes)
    plt.pause(2)  # Pause for 2 seconds before continuing


plt.ioff()  # Turn off interactive mode
plt.show()  # Show the final plot

