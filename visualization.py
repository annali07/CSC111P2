"""
The purpose of this document is to compile the final visualization
and implement the generate_graph() function based on the initial 
data obtained from the interface, including:
    A. Virus Data
        1. infection_rate
        2. incubation_period
        3. death_rate
        4. recovery_days
    B. Population Data
        5. initial_infected_count
        6. population_size
        7. house_density
        8. contact_density
        9. (TODO) policy enforced
    C. Visualization Data
        10. pause
        11. total_days
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from simulation.main_simulation import Simulation, Person, Virus, Policy

numberType = int | float

FAMILY_EDGE = dict(width=2.0, edge_color='blue')


def generate_number_normally(center: numberType, length: numberType, amount: int = 1) -> list[int]:
    length = float(length)
    lowerBound = center - float(length) / 2
    upperBound = center + float(length) / 2
    random_numbers = np.random.normal(loc=center, scale=length/6, size=amount)
    return np.clip(random_numbers, lowerBound, upperBound)


def generate_graph(
    virus_data: dict[str, numberType],
    population_data: dict[str, numberType],
    visualization_data: dict[str, numberType]
) -> None:
    """
    Preconditions:
    - virus_parameter = ["infection_rate",
        "incubation_period", "death_rate", "recovery_days"] are included
        as keys in virus_data
    - population_parameter = ["population_size", "house_density",
        "contact_density", "initial_infected_count"] are keys in population_data
    - visualization_parameter = ["pause", "total_days"] are keys in
        visualization_data
    """
    num_nodes = population_data["population_size"]
    graph = nx.Graph()
    graph.add_nodes_from(range(1, num_nodes + 1))
    assert num_nodes >= 10

    # Initialize interation mode matplotlib
    plt.ion()
    fig, ax = plt.subplots()

    # Initialize Nodes
    _finished_nodes = 0
    _unsampled_nodes = list(range(1, num_nodes + 1))
    house_density = population_data.get("house_density", 3)
    while (_finished_nodes < num_nodes - int(house_density)):

        # Generate a group of family based on house_density
        family_size = generate_number_normally(
            house_density, house_density / 2, 1)[0]
        family_size = int(family_size)
        nodes = random.sample(_unsampled_nodes, family_size)
        _finished_nodes += len(nodes)

        # Remove nodes from sampling candidates
        for i in nodes:
            if not i in nodes:
                continue
            _unsampled_nodes.remove(i)

        # Add Close Contact Edge
        for i in nodes:
            for j in nodes:
                if not graph.has_edge(i, j) and i != j:
                    graph.add_edge(i, j)

    # Deal with edge cases
    for i in _unsampled_nodes:
        for j in _unsampled_nodes:
            if not graph.has_edge(i, j) and i != j:
                graph.add_edge(i, j, **FAMILY_EDGE)

    # Animation
    positions = nx.spring_layout(graph)
    for day in range(1, visualization_data.get("total_days", 30)):
        # Clear current axes and figure (this clears everything from the plot)
        ax.clear()
        fig.clf()

        # Redefine ax to ensure it's correctly linked to the current figure
        ax = fig.add_subplot(111)
        node_colors_dict = {node: "green" for node in graph.nodes()}
        node_colors = [color for node,
                       color in sorted(node_colors_dict.items())]

        nx.draw(graph, pos=positions, node_color=node_colors,
                with_labels=False, ax=ax, node_size=30)

        # Set the title and subtitle
        fig.suptitle('Virus Infection', ha='center')
        ax.set_title(f'The {day}th Day', fontsize=10, ha='center', x=0.5)

        # Draw and pause
        plt.draw()
        plt.pause(visualization_data.get("pause", 0.35))

    # Keep the window open after the loop
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    virus_data = {'infection_rate': 0.3,
                  'incubation_period': 5, 'death_rate': 0.1, 'recovery_days': 7}
    population_data = {'population_size': 550, 'house_density': 3.6, 'contact_density': 5,
                       'initial_infected_count': 6}
    visualization_data = {"total_days": 5}
    generate_graph(virus_data, population_data, visualization_data)
