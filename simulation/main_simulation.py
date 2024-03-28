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
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
import random
from person import Person
from virus import Virus
from policy import Policy
from pygame_helper_functions import InputBox

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption("Virus Spread Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Colors
WHITE = (255, 255, 255)
BLUE = (148, 135, 199)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 120, 150)

# Simulation Parameters (Defaults)
parameters = {
    'infection_rate': 0.3,
    'initial_infected_count': 5,
    'incubation_period': 5,
    'death_rate': 0.02,
    'recovery_days': 7
}

# Layout parameters
slider_start_x = 325
slider_start_y = 162
slider_spacing = 51
label_offset_x = -90
button_width = 150
button_height = 40
button_x = 325
button_y = 500

# Input Box
population_size_box = InputBox(slider_start_x, 97, 200, 40, font)
input_text = ''
# Switch
isolate_infected_btn = Button(screen, slider_start_x, 395, 200, 40, text='Isolate Infected: OFF', fontSize=18, margin=20, inactiveColour=BUTTON_COLOR, pressedColour=(0, 180, 180), radius=20)
clear_neighbors_btn = Button(screen, slider_start_x, 448, 200, 40, text='Clear Neighbors: OFF', fontSize=18, margin=20, inactiveColour=BUTTON_COLOR, pressedColour=(0, 180, 180), radius=20)
# Slider
initial_infected_count_slider = Slider(screen, slider_start_x, slider_start_y, 300, 10, min=1, max=10, step=1)
infection_rate_slider = Slider(screen, slider_start_x, slider_start_y + slider_spacing, 300, 10, min=0.01, max=1.0, step=0.01, initial=0.3)
incubation_period_slider = Slider(screen, slider_start_x, slider_start_y + 2 * slider_spacing, 300, 10, min=1, max=14, step=1, initial=5)
death_rate_slider = Slider(screen, slider_start_x, slider_start_y + 3 * slider_spacing, 300, 10, min=0.01, max=1.0, step=0.01, initial=0.1)
recovery_days_slider = Slider(screen, slider_start_x, slider_start_y + 4 * slider_spacing, 300, 10, min=1, max=14, step=1, initial=7)

start_simulation_button = Button(screen, 300, 520, 250, 50, text='Start Simulation',
                                 fontSize=30, margin=5, inactiveColour=BUTTON_COLOR, pressedColour=(100, 255, 100), radius=20,
                                 onClick=lambda: fetch_parameters())

# Store the state of switches and input text
population_size = int(population_size_box.text) if population_size_box.text.isdigit() else 500
isolate_infected = False
clear_neighbors = False


def fetch_parameters():
    """
    """
    global parameters
    parameters['population_size'] = population_size
    parameters['isolate_infected'] = isolate_infected
    parameters['clear_neighbors'] = clear_neighbors
    parameters['initial_infected_count'] = initial_infected_count_slider.getValue()
    parameters['infection_rate'] = infection_rate_slider.getValue()
    parameters['incubation_period'] = incubation_period_slider.getValue()
    parameters['death_rate'] = death_rate_slider.getValue()
    parameters['recovery_days'] = recovery_days_slider.getValue()

    print(parameters)  # Debugging

    pygame.quit()  # Close the Pygame window
    run_simulation()  # Call the simulation function


# Initialize the virus and policy based on the provided attributes
virus = Virus(incubation_period=5, infection_rate=0.3, death_rate=0.02, recovery_days=7)
policy = Policy(isolate_infected=False, clear_neighbors=False)


def run_simulation():
    """ Initialize each objects by the varibales in params
    """
    virus = Virus(incubation_period=parameters['incubation_period'], infection_rate=parameters['infection_rate'],
                  death_rate=parameters['death_rate'], recovery_days=parameters['recovery_days'])
    policy = Policy(isolate_infected=parameters['isolate_infected'], clear_neighbors=parameters['clear_neighbors'])

    sim = Simulation(population_size=parameters['population_size'], initial_infected_count=parameters['initial_infected_count'],
                     virus=virus, policy=policy)
    # sim.run()


class Simulation:
    """ Main part for the simulation of virus spread.
    """
    population_size: int
    initial_infected_count: int
    persons: {int: Person}

    def __init__(self, population_size: int, initial_infected_count: int, virus: Virus, policy: Policy) -> None:
        self.population_size = population_size
        self.G = nx.Graph()
        self.persons = {i: Person() for i in range(population_size)}
        self.virus = virus
        self.policy = policy
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


def draw_text(text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print(f"Clicked at: {mouse_pos}")
            if 303 <= mouse_pos[0] <= 548 and 521 <= mouse_pos[1] <= 568:
                fetch_parameters()
                running = False
                pygame.quit()
                sys.exit()

        population_size_box.handle_event(event)

    screen.fill(WHITE)

    # Draw labels for sliders and buttons
    draw_text('Population Size:', (50, 105), font)
    draw_text('Initial Infected Count:', (50, 155), font)
    draw_text('Infection Rate:', (50, 205), font)
    draw_text('Incubation Period:', (50, 255), font)
    draw_text('Death Rate:', (50, 305), font)
    draw_text('Recovery Days:', (50, 355), font)
    draw_text('Isolate Infected:', (50, 405), font)
    draw_text('Clear Neighbors:', (50, 455), font)

    # Draw and update all UI elements
    population_size_box.draw(screen)
    initial_infected_count_slider.listen(events)
    initial_infected_count_slider.draw()
    infection_rate_slider.listen(events)
    infection_rate_slider.draw()
    incubation_period_slider.listen(events)
    incubation_period_slider.draw()
    death_rate_slider.listen(events)
    death_rate_slider.draw()
    recovery_days_slider.listen(events)
    recovery_days_slider.draw()
    isolate_infected_btn.listen(events)
    isolate_infected_btn.draw()
    clear_neighbors_btn.listen(events)
    clear_neighbors_btn.draw()
    start_simulation_button.listen(events)
    start_simulation_button.draw()

    pygame.display.flip()
    clock.tick(30)
