import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# edge_list = [(1, 2), (2, 3), (3, 4), (1, 4)]

G = nx.Graph()
G.add_nodes_from(range(1, 15))  # Add nodes 1-7
# G.add_edges_from(edge_list)

# Initialize positions
positions = nx.spring_layout(G, seed=42)

# Turn on interactive mode
plt.ion()

# Set up the plot
fig, ax = plt.subplots()

for i in range(1, 15):
    # Add edge if within range
    if i < 12:
        G.add_edge(i, i + 1)

    # Clear current axes and figure (this clears everything from the plot)
    ax.clear()
    fig.clf()

    # Redefine ax to ensure it's correctly linked to the current figure
    ax = fig.add_subplot(111)

    # Update node colors
    node_colors = ['red' if node in [i, i + 1] else 'blue' for node in G.nodes()]

    # Draw the graph on the current axes
    nx.draw(G, pos=positions, node_color=node_colors, with_labels=True, ax=ax)

    # Set the title and subtitle
    fig.suptitle('Main Title Here')  # Main title
    ax.set_title(f'The {i}th Day', fontsize=10)  # Subtitle

    # Draw and pause
    plt.draw()
    plt.pause(2)

# Keep the window open after the loop
plt.ioff()
plt.show()
