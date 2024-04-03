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

        contact density = 1 - isolation force 


    Colors: green (healthy), red (infected), blue (recorved), black (dead), purple (infected, but not detected)
    Question:
        1. what is the significance of blue nodes? 
        2. what is the probability of triggering incubation period?
    
    attributes = [
        ["Attribute", "Description", "Possible Values"],
        ["status", "Indicates the health status of a person.", "'healthy', 'infected', 'recovered', 'dead', 'incubated'"],
        ["days_infected", "Tracks how many days a node has been infected.", "Integer values starting from 0"],
        ["node_color", "Used for visualization, indicates the health status of a person by color.", "'green', 'red', 'blue', 'black', 'purple'"],
        ["family", "Indicates the family group of a person. Nodes within the same family have closer connections.", "Integer values, -1 for no family"]
    ]

    isolation foce affects family by lowering infection rate, affects others by reducing added edge? 
    too little edge added? unreasonable? 

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


def initialize_edges(graph: nx.Graph, contact_density: int, isolation_force: float) -> None:
    """
    Initialize the edges of the graph
    """
    new_edges = []

    for u in graph.nodes():
        if graph.nodes[u]['status'] == 'dead':
            continue
        
        potential_connections = [v for v in graph.nodes() if
                                u != v and 
                                graph.nodes[v]['status'] not in ['dead'] and
                                not graph.has_edge(u, v)]
        
        new_contact_density = contact_density * (1 - isolation_force)
        num = min(int(generate_number_normally(new_contact_density, new_contact_density)[0]), 10)
        num_new_edges = min(num - graph.degree(u), len(potential_connections))

        if num_new_edges > 0:
            # print(num_new_edges)
            n_edges = random.sample(potential_connections, num_new_edges)

            for node in n_edges:
                new_edges.append((u, node))
                graph.add_edge(u, node, edge_color=(0,0,0,0.3))
    return new_edges    


def update_day(graph: nx.Graph, infection_rate: float, death_rate: float, recovery_days: int, contact_density: int, isolation_force: float, incubation_period: int, edges: list) -> None:
    """
    Update the graph based on the current day
    
    1. Check all existing edges and color the node
    2. Randomly choose infected and let die 
    2. Reorder the contacting edges
    
    """
    all_edges = list(graph.edges())

    for u, v in all_edges:
        if graph.nodes[u]['status'] == 'infected' or graph.nodes[u]['status'] == 'incubated':
            if graph.nodes[v]['status'] != 'infected' and graph.nodes[v]['status'] != 'dead':          
                if random.random() < infection_rate:
                    if random.random() < 0.5:
                        graph.nodes[v]['status'] = 'incubated'
                        graph.nodes[v]['node_color'] = 'purple'
                        graph.nodes[v]['days_infected'] = 0
                    else:
                        graph.nodes[v]['status'] = 'infected'
                        graph.nodes[v]['node_color'] = 'red' 
                        graph.nodes[v]['days_infected'] = 0

        elif graph.nodes[v]['status'] == 'infected' or graph.nodes[v]['status'] == 'incubated':
            if graph.nodes[u]['status'] != 'infected' and graph.nodes[u]['status'] != 'dead':
                if random.random() < infection_rate:
                    if random.random() < 0.5:
                        graph.nodes[u]['status'] = 'incubated'
                        graph.nodes[u]['node_color'] = 'purple'
                        graph.nodes[u]['days_infected'] = 0
                    else:
                        graph.nodes[u]['status'] = 'infected'
                        graph.nodes[u]['node_color'] = 'red'
                        graph.nodes[u]['days_infected'] = 0

    infected_nodes = [node for node, attrs in graph.nodes(data=True) if attrs.get('status') == 'infected']
    for node in infected_nodes:
        if graph.nodes[node]['days_infected'] >= recovery_days:
            if random.random() < death_rate:
                graph.nodes[node]['status'] = 'dead'
                graph.nodes[node]['node_color'] = 'black'
            else:
                graph.nodes[node]['status'] = 'recovered'
                graph.nodes[node]['node_color'] = 'blue'
        else:
            graph.nodes[node]['days_infected'] += 1

    incubated_nodes = [node for node, attrs in graph.nodes(data=True) if attrs.get('status') == 'incubated']
    for node in incubated_nodes:
        if graph.nodes[node]['days_infected'] >= incubation_period:
            graph.nodes[node]['status'] = 'infected'
            graph.nodes[node]['node_color'] = 'red'
            graph.nodes[node]['days_infected'] = 0
        else:
            graph.nodes[node]['days_infected'] += 1


    graph.remove_edges_from(edges)

    new_edges = []
    max_num = 0

    for u in graph.nodes():
        if graph.nodes[u]['status'] == 'dead':
            continue
        
        # a list of nodes
        potential_connections = [v for v in graph.nodes() if
                                (v != u and 
                                graph.nodes[v]['status'] != 'dead' and
                                not graph.has_edge(u, v))]
        
        new_contact_density = contact_density * (1 - isolation_force)
        num = min(int(generate_number_normally(new_contact_density, new_contact_density)[0]), 10)
        num_new_edges = min(num - graph.degree(u), len(potential_connections))

        if num_new_edges > 0:
            if num_new_edges > max_num:
                max_num = num_new_edges
                print(num_new_edges)
            n_edges = random.sample(potential_connections, num_new_edges)
            print(potential_connections)
            for node in n_edges:
                new_edges.append((u, node))
                graph.add_edge(u, node, edge_color=(0,0,0,0.3)) 
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
    initial_infected_count = int(data.get("initial_infected_count", 5))  # Assuming default 0
    incubation_period = int(data.get("incubation_period", 5))  # Assuming default 0
    death_rate = float(data.get("death_rate", 0.02))  # Assuming default 0
    recovery_days = int(data.get("recovery_days", 7))  # Assuming default 0
    population_size = int(min(max(data.get("population_size", 500), 10), 1000))
    isolate_force = float(data.get("isolate_force", 0.0))  # Assuming default 0
    house_density = density_mapping.get(data["house_density"].lower(), 2)
    contact_density = int(data.get("contact_density", 5))  # Assuming default 0

    # Initialize the graph
    graph = nx.Graph()
    graph.add_nodes_from(range(1, population_size + 1))
    num_nodes = graph.number_of_nodes()

    plt.ion()
    fig, ax = plt.subplots(figsize=(15, 10))

    # Initialize family members
    initialize_family(graph, num_nodes, house_density)
    initialize_infected(graph, initial_infected_count)

    # Animation
    positions = nx.spring_layout(graph, scale=5, k = 1.0/(len(graph.nodes())**0.5), iterations=20, seed=42)
    edges = initialize_edges(graph, contact_density, isolate_force)
    for day in range(1, 101):
        ax.clear()
        fig.clf()

        # Redefine ax to ensure it's correctly linked to the current figure
        ax = fig.add_subplot(111)
        
        # Update the graph
        edges = update_day(graph, infection_rate, death_rate, recovery_days,contact_density, isolate_force, incubation_period, edges)
        node_colors = [graph.nodes[node]['node_color'] for node in graph.nodes()]
        edge_colors = [graph.edges[edge]['edge_color'] for edge in graph.edges()]
        nx.draw(graph, pos=positions, node_color=node_colors,
                with_labels=False, ax=ax, node_size=10, edge_color=edge_colors)
        
        # Set the title and subtitle
        infected = sum([1 for node in graph.nodes() if graph.nodes[node]['status'] == 'infected'])
        dead = sum([1 for node in graph.nodes() if graph.nodes[node]['status'] == 'dead'])

        fig.suptitle('Virus Infection', ha='center')
        fig.text(0.5, 0.94, f'The {day}th Day', ha='center', va='center', fontsize=10)  # Subtitle below main title
        fig.text(0.5, 0.9, f'Infected: {infected} / {population_size - dead}', ha='center', va='center', fontsize=10)  # Second subtitle below the first subtitle

        # Draw and pause
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05)
        plt.draw()
        plt.pause(0.5)

    # Keep the window open after the loop
    plt.ioff()
    plt.show()