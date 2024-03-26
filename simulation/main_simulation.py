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
import sys, pygame

def simulate_spread(days, initial_infected_count):
    """Main simulation method
    """
    # Initialize virus, people, and graph
    virus = Virus(incubation_period=5, infection_rate=0.3, death_rate=0.02)
    policy = Policy(isolate_infected=True, clear_neighbors=False)
    population_graph = Graph()

    # Add people and connections
    for i in range(100):
        population_graph.add_person(i, Person())

    # # Randomly infect initial set of people
    # initial_infected = random.sample(population_graph.vertices.keys(), initial_infected_count)
    # for person_id in initial_infected:
    #     population_graph.vertices[person_id].status = "incubation"
    #
    # Main simulation loop
    for day in range(days):
        population_graph.spread_virus()
        population_graph.apply_policy(policy)
        # todo
        time.sleep(1)  # Simulate one day per second


if __name__ == "__main__":
    simulate_spread(days=45, initial_infected_count=5)
