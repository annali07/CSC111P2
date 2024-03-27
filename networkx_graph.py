import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# edge_list = [(1, 2), (2, 3), (3, 4), (1, 4)]


def generate_graph(dt: dict) -> None:
    text = dt['txt']
    # G = nx.Graph() # generate different real-world model graphs
    G = nx.watts_strogatz_graph(100, 4, 0.1)
    # G.add_nodes_from(range(1, 51))

    # G.add_edges_from(edge_list)

    # Initialize positions
    positions = nx.random_layout(G)
    # positions = nx.spring_layout(G, k=1.0/(len(G.nodes())**0.5), iterations=20)
    # positions = nx.spectral_layout(G)'


    plt.ion()
    fig, ax = plt.subplots()

    for i in range(1, 50):
        # # add edge
        # node_a, node_b = random.sample(range(1, 97), 2)
        # if not G.has_edge(node_a, node_b):
        #     G.add_edge(node_a, node_b)

        # Clear current axes and figure (this clears everything from the plot)
        ax.clear()
        fig.clf()

        # Redefine ax to ensure it's correctly linked to the current figure
        ax = fig.add_subplot(111)

        # Update node colors
        node_colors = ['red' if node in [i, i + 1] else 'blue' for node in G.nodes()]

        # Draw the graph on the current axes
        nx.draw(G, pos=positions, node_color=node_colors, with_labels=False, ax=ax, node_size=50)

        # Set the title and subtitle
        # fig.suptitle('Virus Infection')
        fig.suptitle(text)
        ax.set_title(f'The {i}th Day + {dt['value']}', fontsize=10)  # Subtitle

        # Draw and pause
        plt.draw()
        plt.pause(0.1)

    # Keep the window open after the loop
    plt.ioff()
    plt.show()
