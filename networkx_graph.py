import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# edge_list = [(1, 2), (2, 3), (3, 4), (1, 4)]

def generate_graph(dt: dict, pause: float = .35) -> None:
    num_nodes = int(dt['txt'])
    num_color = int(dt['value'])
    G = nx.Graph() # generate different real-world model graphs
    # G = nx.watts_strogatz_graph(100, 4, 0.1)
    G.add_nodes_from(range(1, num_nodes))

    # G.add_edges_from(edge_list)

    # Initialize positions
    positions = nx.random_layout(G)
    # positions = nx.spring_layout(G, k=1.0/(len(G.nodes())**0.5), iterations=20)
    # positions = nx.spectral_layout(G)'


    plt.ion()
    fig, ax = plt.subplots()

    for i in range(1, num_nodes):
        # # add edge
        node_a, node_b = random.sample(range(1, num_nodes), 2)
        if not G.has_edge(node_a, node_b):
            G.add_edge(node_a, node_b)

        # Clear current axes and figure (this clears everything from the plot)
        ax.clear()
        fig.clf()

        # Redefine ax to ensure it's correctly linked to the current figure
        ax = fig.add_subplot(111)

        # Update node colors
        node_colors = {node: 'red' if node in [i, i + 1] else 'blue' for node in G.nodes()}
        random_nodes = random.sample(range(1, num_nodes), num_color)
        for node in random_nodes:
            node_colors[node] = random.choice(['red', 'blue'])
        # node_colors = ['red' if node in [i, i + 1] else 'blue' for node in G.nodes()]
        node_colors = [color for node, color in sorted(node_colors.items())]

        # Draw the graph on the current axes
        nx.draw(G, pos=positions, node_color=node_colors, with_labels=False, ax=ax, node_size=50)

        # Set the title and subtitle
        fig.suptitle('Virus Infection', ha='center')
        ax.set_title(f'The {i}th Day', fontsize=10, ha='center', x=0.5)

        # Draw and pause
        plt.draw()
        plt.pause(pause)

    # Keep the window open after the loop
    plt.ioff()
    plt.show()
