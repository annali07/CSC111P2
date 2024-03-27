"""CSC111 Project 2: Main Simulation

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 2. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
import random
from person import Person
from virus import Virus
from policy import Policy

# Adjust as needed
population_size = 500
initial_infected_count = 10
simulation_days = 50

# Initialize the virus and policy based on the provided attributes
virus = Virus(incubation_period=5, infection_rate=0.3, death_rate=0.02, recovery_days=7)
policy = Policy(isolate_infected=False, clear_neighbors=False)


class Simulation:
    """ Main part for the simulation of virus spread.
    """
    population_size: int
    initial_infected_count: int
    persons: {int: Person}

    def __init__(self, population_size: int, initial_infected_count: int) -> None:
        self.population_size = population_size
        self.G = nx.Graph()
        self.persons = {i: Person() for i in range(population_size)}
        self.initial_infected(initial_infected_count)
        self.create_connections()

    def initial_infected(self, initial_infected_count: int) -> None:
        """ Method to set the initial infected people
        """
        infected_ids = random.sample(list(self.persons.keys()), initial_infected_count)
        for i in infected_ids:
            self.persons[i].status = "incubation"

    def create_connections(self) -> None:
        """ Method to creating the connections within the population
        """
        pass

    def spread_virus(self) -> None:
        """ Method for
        """
        for person in self.persons:
            if person.status in ["incubation", "infected"]:
                for connected_person in person.connections:
                    if connected_person.status == "uninfected" and random.random() < virus.infection_rate:
                        connected_person.status = "incubation"

    def update_status(self) -> None:
        """ Update status
        """
        for person in self.persons:
            person.update_status(virus)

    def apply_policy(self) -> None:
        """ Implementation for isolation policy
        """
        pass

    def draw(self) -> None:
        """ Draw or update the graph visualization for the current day
        """
        pass


if __name__ == "__main__":
    sim = Simulation(population_size, initial_infected_count)
