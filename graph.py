import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# edge_list = [(1, 2), (2, 3), (3, 4), (1, 4)]

G = nx.Graph()
G.add_nodes_from(range(1, 100))  # Add nodes 1-7
# G.add_edges_from(edge_list)

# Initialize positions
positions = nx.random_layout(G, seed=42)

# Turn on interactive mode
plt.ion()

# Set up the plot
fig, ax = plt.subplots()

for i in range(1, 98):
    # Add edge if within range
    node_a, node_b = random.sample(range(1, 97), 2)
    
    # Check if the edge already exists before adding it
    if not G.has_edge(node_a, node_b):
        G.add_edge(node_a, node_b)

    # Clear current axes and figure (this clears everything from the plot)
    ax.clear()
    fig.clf()

    # Redefine ax to ensure it's correctly linked to the current figure
    ax = fig.add_subplot(111)

    # Update node colors
    node_colors = ['red' if node in [i, i + 1] else 'blue' for node in G.nodes()]

    # Draw the graph on the current axes
    nx.draw(G, pos=positions, node_color=node_colors, with_labels=True, ax=ax, node_size=100)

    # Set the title and subtitle
    fig.suptitle('Virus Infection')  # Main title
    ax.set_title(f'The {i}th Day', fontsize=10)  # Subtitle

    # Draw and pause
    plt.draw()
    plt.pause(0.1)

# Keep the window open after the loop
plt.ioff()
plt.show()
