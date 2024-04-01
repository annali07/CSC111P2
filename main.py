"""
CSC111 Project 2: Virus Spread Simulation

"""
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
import random
from simulation import Virus, Person, Policy


class InputBox:
    """
    A class for creating and managing an interactive input box in a Pygame application.

    This input box allows users to enter text through keyboard inputs. It supports basic text editing features like
    backspacing and displays the current text within a rectangular input field.
    """

    def __init__(self, x: int, y: int, w: int, h: int, font, text: str = '') -> None:
        self.font = font
        self.BLUE = (148, 135, 199)
        self.BLACK = (0, 0, 0)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.BLACK
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        Handles events related to the input box, such as mouse clicks and keyboard inputs.

        This method allows the input box to respond to mouse clicks for activation/deactivation and keyboard inputs
        for text editing.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.BLUE if self.active else self.BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        """
        Updates the input box's width to fit the current text.
        """
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        """
        Draws the input box and the current text on the specified screen.
        """
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class VirusSimulationApp:
    """
    A class to encapsulate the virus spread simulation application, including its UI elements and simulation logic.
    """
    screen: pygame.Surface
    clock: pygame.time.Clock
    font: pygame.font.Font
    WHITE: tuple[int, int, int]
    BUTTON_COLOR: tuple[int, int, int]
    network_typology_status: str
    parameters: dict[str, any]

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 650))
        pygame.display.set_caption("Virus Spread Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.WHITE = (255, 255, 255)
        self.BUTTON_COLOR = (0, 120, 150)
        self.network_typology_status = "SMALL-WORLD"
        self.parameters = self.default_parameters()
        self.setup_ui_elements()

    def default_parameters(self) -> dict[str, any]:
        """
        Defines the default parameters for the simulation.

        Returns:
            dict: A dictionary containing default values for various simulation parameters.
        """
        return {
            'infection_rate': 0.3,
            'initial_infected_count': 5,
            'incubation_period': 5,
            'death_rate': 0.02,
            'recovery_days': 7,
            'population_size': 500,
            'isolate_force': 0.0,
            'network_typology': self.network_typology_status
        }

    def setup_ui_elements(self):
        """
        Sets up the user interface elements for the simulation.
        """
        # Layout parameters for positioning UI elements
        slider_start_x = 325  # X-coordinate for the starting position of sliders
        slider_start_y = 162  # Y-coordinate for the starting position of the first slider
        slider_spacing = 51   # Vertical spacing between sliders

        # Input Box for population size
        # This creates an input box for users to enter the population size, positioned at the top.
        self.population_size = 500
        self.population_size_box = InputBox(slider_start_x, 97, 200, 40, self.font)
        self.input_text = ''     # Variable to store the input text from the user

        # Button for changing network topology
        # Allows users to cycle through network topology types( SMALL-WORLD / RANDOM / SCALE-FREE ).
        self.network_typology_btn = Button(self.screen, slider_start_x, 448, 200, 40,
                                           text=f'{self.network_typology_status}', fontSize=22, margin=20,
                                           inactiveColour=self.BUTTON_COLOR, pressedColour=(0, 180, 180), radius=20)

        # Sliders for simulation parameters
        # Allow users to adjust various simulation parameters such as the initial infected count, infection rate, etc.
        self.initial_infected_count_slider = Slider(self.screen, slider_start_x, slider_start_y,
                                                    300, 10, min=1, max=25, step=1, initial=10)
        self.infection_rate_slider = Slider(self.screen, slider_start_x, slider_start_y + slider_spacing,
                                            300, 10, min=0.01, max=1.0, step=0.01, initial=0.3)
        self.incubation_period_slider = Slider(self.screen, slider_start_x, slider_start_y + 2 * slider_spacing,
                                               300, 10, min=1, max=14, step=1, initial=5)
        self.death_rate_slider = Slider(self.screen, slider_start_x, slider_start_y + 3 * slider_spacing,
                                        300, 10, min=0.01, max=1.0, step=0.01, initial=0.1)
        self.recovery_days_slider = Slider(self.screen, slider_start_x, slider_start_y + 4 * slider_spacing,
                                           300, 10, min=1, max=14, step=1, initial=7)
        self.isolation_force_slider = Slider(self.screen, slider_start_x, slider_start_y + 5 * slider_spacing,
                                             300, 10, min=0.00, max=1.0, step=0.01, initial=0.0)

        # Button for starting the simulation
        # This button triggers the fetching of parameters and potentially starts the simulation.
        self.start_simulation_button = Button(self.screen, 300, 520, 250, 50,
                                              text='Start Simulation', fontSize=30, margin=5,
                                              inactiveColour=self.BUTTON_COLOR, pressedColour=(100, 255, 100),
                                              radius=20, onClick=self.fetch_parameters)

    def toggle_network_typology(self):
        """
        Toggles the network typology status among predefined types.
        """
        if self.network_typology_status == "SMALL-WORLD":
            self.network_typology_status = "RANDOM"
        elif self.network_typology_status == "RANDOM":
            self.network_typology_status = "SCALE-FREE"
        else:
            self.network_typology_status = "SMALL-WORLD"
        self.parameters['network_typology'] = self.network_typology_status
        self.network_typology_btn.setText(self.network_typology_status)

    def fetch_parameters(self):
        """
        Fetches simulation parameters from various UI elements and updates the global `parameters` dictionary.

        This function gathers user-defined values for the population size, initial infected count, infection rate,
        incubation period, death rate, recovery days, isolation force, and network topology status from corresponding
        UI sliders and status indicators. These values are used to configure the simulation environment.

        After collecting and updating these parameters, it prints the updated `parameters` dictionary for debugging,
        closes the Pygame window, and initiates the simulation by calling `run_simulation()`.
        """
        # Fetching values from UI components and updating the 'parameters' dictionary
        self.parameters['population_size'] = self.population_size
        self.parameters['initial_infected_count'] = self.initial_infected_count_slider.getValue()
        self.parameters['infection_rate'] = self.infection_rate_slider.getValue()
        self.parameters['incubation_period'] = self.incubation_period_slider.getValue()
        self.parameters['death_rate'] = self.death_rate_slider.getValue()
        self.parameters['recovery_days'] = self.recovery_days_slider.getValue()
        self.parameters['isolate_force'] = self.isolation_force_slider.getValue()
        self.parameters['network_typology'] = self.network_typology_status
        pygame.quit()  # Close the Pygame window to proceed with the simulation

    def run_simulation(self):
        """
        Initializes and runs the simulation based on the current configuration.

        This function creates instances of the `Virus` and `Policy` classes using the parameters
        specified in the global `parameters` dictionary. It then initializes a `Simulation` object
        with the population size, initial infected count, `Virus` instance, and `Policy` instance.

        The simulation environment is prepared by instantiating the necessary components with their
        respective parameters.
        """
        self.fetch_parameters()
        print("Simulation parameters:", self.parameters)

        # Creating instances of Virus and Policy with their respective parameters
        virus = Virus(
            incubation_period=self.parameters['incubation_period'],
            infection_rate=self.parameters['infection_rate'],
            death_rate=self.parameters['death_rate'],
            recovery_days=self.parameters['recovery_days']
        )
        policy = Policy(
            isolate_force=self.parameters['isolate_force']
        )

        sim = Simulation(
            population_size=self.parameters['population_size'],
            initial_infected_count=self.parameters['initial_infected_count'],
            virus=virus,
            policy=policy
        )

        # sim.run()

    def draw_text(self, text: str, position: tuple[int, int], color: tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Draws text on the Pygame screen at a specified position.
        """
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def main_game_loop(self) -> None:
        """
        Main Interface Loop Function
        """
        running = True
        while running:
            # Get all the events from the event queue
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    # Terminate the program if the close button is clicked
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse button down events
                    mouse_pos = event.pos  # Get the position of the mouse click
                    print(f"Clicked at: {mouse_pos}")  # Debugging: print the click position

                    # Check if the click is within the bounds of the 'Start Simulation' button
                    if 303 <= mouse_pos[0] <= 548 and 521 <= mouse_pos[1] <= 568:
                        self.population_size = int(self.population_size_box.text) \
                            if self.population_size_box.text.isdigit() else 500
                        self.run_simulation()  # Fetch simulation parameters from the UI
                        pygame.quit()
                        sys.exit()

                    # Check if the click is within the bounds of the 'Change Network Typology' button
                    elif 327 <= mouse_pos[0] <= 524 and 450 <= mouse_pos[1] <= 486:
                        # Rotate through network topology statuses
                        self.toggle_network_typology()

                self.population_size_box.handle_event(event)

            # Clear the screen with a white background
            self.screen.fill(self.WHITE)
            # Fetch and format the current values from sliders
            initial_infected_count_output = str(self.initial_infected_count_slider.getValue())
            infection_rate_output = str(round(self.infection_rate_slider.getValue() * 100)) + "%"
            incubation_period_output = str(self.incubation_period_slider.getValue())
            death_rate_output = str(round(self.death_rate_slider.getValue() * 100)) + "%"
            recovery_days_output = str(self.recovery_days_slider.getValue())
            isolation_force_output = str(round(self.isolation_force_slider.getValue() * 100)) + "%"

            labels_and_values = [
                ('Population Size:', None),
                ('Initial Infected Count:', initial_infected_count_output),
                ('Infection Rate:', infection_rate_output),
                ('Incubation Period:', incubation_period_output),
                ('Death Rate:', death_rate_output),
                ('Recovery Days:', recovery_days_output),
                ('Isolation Force:', isolation_force_output),
                ('Network Typology:', None)
            ]
            for i, (label, value) in enumerate(labels_and_values):
                self.draw_text(label, (50, 105 + 50 * i))
                if value:
                    self.draw_text(value, (640, 105 + 50 * i))

            ui_elements = [
                self.population_size_box,
                self.initial_infected_count_slider,
                self.infection_rate_slider,
                self.incubation_period_slider,
                self.death_rate_slider,
                self.recovery_days_slider,
                self.isolation_force_slider,
                self.start_simulation_button
            ]
            for element in ui_elements:
                if element == self.population_size_box:
                    self.population_size_box.draw(self.screen)
                else:
                    element.listen(events)
                    element.draw()

            pygame_widgets.update(events)
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


class Simulation:
    """
    Represents the main framework for simulating the spread of a virus within a population.

    Attributes:
        population_size (int): The total number of people in the population.
        initial_infected_count (int): The number of initially infected individuals.
        persons (dict[int, Person]): A dictionary mapping each person's ID to their respective Person object.
        virus (Virus): An instance of the Virus class, containing virus-specific parameters.
        policy (Policy): An instance of the Policy class, representing the policy to be applied during the simulation.
    """

    def __init__(self, population_size: int, initial_infected_count: int, virus: Virus, policy: Policy) -> None:
        self.population_size = population_size
        self.G = nx.Graph()
        self.persons = {i: Person() for i in range(population_size)}
        self.virus = virus
        self.policy = policy
        self.initial_infected(initial_infected_count)
        self.create_connections()

    def initial_infected(self, initial_infected_count: int) -> None:
        """
        Randomly selects a subset of the population to be initially infected with the virus.
        """
        infected_ids = random.sample(list(self.persons.keys()), initial_infected_count)
        for i in infected_ids:
            self.persons[i].status = "incubation"

    def create_connections(self) -> None:
        """
        Creates connections between individuals in the population to simulate their interactions.
        """
        pass

    def spread_virus(self) -> None:
        """
        Simulates the transmission of the virus between connected individuals based on the infection rate.
        """
        for person_id, person in self.persons.items():
            if person.status in ["incubation", "infected"]:
                for neighbor_id in self.G.neighbors(person_id):
                    neighbor = self.persons[neighbor_id]
                    if neighbor.status == "uninfected" and random.random() < self.virus.infection_rate:
                        neighbor.status = "incubation"

    def update_status(self) -> None:
        """
        Updates the health status of each individual in the population, considering the virus's effects and recovery.
        """
        for person in self.persons.values():
            person.update_status(self.virus)

    def apply_policy(self) -> None:
        """
        Applies the defined policy (e.g., isolation) to mitigate the spread of the virus within the population.
        """
        pass


if __name__ == "__main__":

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],     # the names (strs) of functions that call print/open/input
    })

    app = VirusSimulationApp()
    app.main_game_loop()
