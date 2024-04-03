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
            low = 2
            medium = 4
            high = 6
        8. contact_density
            every day, how many edge a random node is connected to
            (1 - 10)
        9. isolation_force
            force low -> divide contact density by 2
            force medium -> divide contact density by 4
            force high -> divide contact density by 6
                isolation within house
    C. Visualization Data
        10. pause (time between each day)
        11. total_days

    five colors: green (healthy), red (infected), blue (recorved), black (dead), purple (infected, but not detected)
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from simulation import Person, Virus, Policy

numberType = int | float | str

# change edge color - edge between family members, 
FAMILY_EDGE = dict(width=2.0, edge_color='blue')

# pass in contact density as length, 
def generate_number_normally(center: numberType, length: numberType, amount: int = 1) -> list[int]:
    length = float(length)
    lowerBound = center - float(length) / 2
    upperBound = center + float(length) / 2
    random_numbers = np.random.normal(loc=center, scale=length/6, size=amount)
    return np.clip(random_numbers, lowerBound, upperBound)


def initialize_family(graph: nx.Graph, num_nodes: int, house_density: int) -> None:
    """
    Initialize a group of family members and connect them with edges
    """
    # Initialize Nodes
    _finished_nodes = 0
    _unsampled_nodes = list(graph.nodes())
    idx = 0
    # Generate a group of family based on house_density
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
                    graph.edges[i, j]['edge_color'] = 'blue'
                    graph.edges[i, j]['relationship'] = 'family'
                    graph.nodes[i]['family'] = idx
                    graph.nodes[j]['family'] = idx
                    idx += 1
    
    for i in graph.nodes():
        if not i in nodes:
            graph.nodes[i]['family'] = -1

    # # Deal with edge cases
    # for i in _unsampled_nodes:
    #     for j in _unsampled_nodes:
    #         if not graph.has_edge(i, j) and i != j:
    #             graph.add_edge(i, j, **FAMILY_EDGE)


def initialize_infected(graph: nx.Graph, initial_infected_count: int) -> None:
    """
    Initialize a group of infected people
    """
    infected_nodes = random.sample(list(graph.nodes()), initial_infected_count)
    for node in graph.nodes():
        if node in infected_nodes:
            graph.nodes[node]['status'] = 'infected'
            graph.nodes[node]['days_infected'] = 0
            graph.nodes[node]['node_color'] = 'red'
        else:
            graph.nodes[node]['status'] = 'healthy'
            graph.nodes[node]['node_color'] = 'green'


def initialize_edges(graph: nx.Graph, contact_density: int) -> None:
    """
    Initialize the edges of the graph
    """
    potential_edges = [(u, v) for u in graph.nodes() for v in graph.nodes() if u != v]
    edges = random.sample(potential_edges, contact_density)
    for u, v in edges:
        graph.add_edge(u, v, edge_color='black')
    return edges


def update_day(graph: nx.Graph, infection_rate: float, edges: list) -> None:
    """
    Update the graph based on the current day
    
    1. Check all existing edges and color the node
    2. Randomly choose infected and let die 
    2. Reorder the contacting edges
    
    """
    for u, v in edges:
        if graph.nodes[u]['status'] == 'infected':
            if graph.nodes[v]['status'] != 'infected':
                rand = random.random()
                print(rand, infection_rate)                
                if rand < infection_rate:
                    graph.nodes[v]['status'] = 'infected'
                    graph.nodes[v]['node_color'] = 'red'  

        elif graph.nodes[v]['status'] == 'infected':
            if graph.nodes[u]['status'] != 'infected':
                if random.random() < infection_rate:
                    graph.nodes[u]['status'] = 'infected'
                    graph.nodes[u]['node_color'] = 'red'
    



    graph.remove_edges_from(edges)

    potential_new_edges = [(u, v) for u in graph.nodes() for v in graph.nodes() if \
(u != v and graph.nodes[u]['family'] != graph.nodes[v]['family']) or (graph.nodes[u]['family'] == -1 or graph.nodes[v]['family'] == -1)]
    
    new_edges = random.sample(potential_new_edges, 10)
    for u, v in new_edges:
        if u != v:
            graph.add_edge(u, v, edge_color='black')
    
    return new_edges
    

def generate_graph(
        data: dict[str, numberType]
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
    density_mapping = {
        "high": 6,
        "medium": 4,
        "low": 2,
    }

    # Add default value
    infection_rate = float(data.get("infection_rate", 0.3))
    initial_infected_count = int(data.get("initial_infected_count", 0))  # Assuming default 0
    incubation_period = int(data.get("incubation_period", 0))  # Assuming default 0
    death_rate = float(data.get("death_rate", 0))  # Assuming default 0
    recovery_days = int(data.get("recovery_days", 0))  # Assuming default 0

    population_size = int(max(data.get("population_size", 10), 10))
    isolate_force = int(data.get("isolate_force", 0))  # Assuming default 0
    house_density = density_mapping.get(data["house_density"].lower(), 2)
    contact_density = int(data.get("contact_density", 0))  # Assuming default 0

    # Initialize the graph
    graph = nx.Graph()
    graph.add_nodes_from(range(1, population_size + 1))
    num_nodes = graph.number_of_nodes()

    plt.ion()
    fig, ax = plt.subplots()

    # Initialize family members
    initialize_family(graph, num_nodes, house_density)
    initialize_infected(graph, initial_infected_count)

    # Animation
    positions = nx.spring_layout(graph, scale=5, k = 1.0/(len(graph.nodes())**0.5), iterations=20, seed=42)
    edges = initialize_edges(graph, contact_density)
    for day in range(1, 91):
        ax.clear()
        fig.clf()

        # Redefine ax to ensure it's correctly linked to the current figure
        ax = fig.add_subplot(111)
        
        edges = update_day(graph, infection_rate, edges)

        node_colors = [graph.nodes[node]['node_color'] for node in graph.nodes()]
        edge_colors = [graph.edges[edge]['edge_color'] for edge in graph.edges()]
        nx.draw(graph, pos=positions, node_color=node_colors,
                with_labels=False, ax=ax, node_size=10, edge_color=edge_colors)
        
        infected = sum([1 for node in graph.nodes() if graph.nodes[node]['status'] == 'infected'])
        # Set the title and subtitle
        fig.suptitle('Virus Infection', ha='center')
        ax.set_title(f'The {day}th Day', fontsize=10, ha='center', x=1.0)
        ax.set_title(f'Infected: {infected} / {population_size}', fontsize=10, ha='center', x=0.5)


        # Draw and pause
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05)
        plt.draw()
        plt.pause(0.5)

    # Keep the window open after the loop
    plt.ioff()
    plt.show()


# if __name__ == "__main__":
    # virus_data = {'infection_rate': 0.3,
    #               'incubation_period': 5, 'death_rate': 0.1, 'recovery_days': 7}
    # population_data = {'population_size': 550, 'house_density': 3.6, 'contact_density': 5,
    #                    'initial_infected_count': 6}
    # visualization_data = {"total_days": 5}
    # generate_graph(virus_data, population_data, visualization_data)