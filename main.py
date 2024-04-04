"""
CSC111 Project 2: Virus Spread Simulation

Lowest population = 10

"""
import sys
import random
from typing_extensions import Any
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
import networkx as nx
from simulation import Virus, Person, Policy
from visualization import generate_graph


class InputBox:
    """
    A class for creating and managing an interactive input box in a Pygame application.

    This input box allows users to enter text through keyboard inputs. It supports basic text editing features like
    backspacing and displays the current text within a rectangular input field.
    """

    font: pygame.font.Font
    blue: tuple
    black: tuple
    rect: pygame.Rect
    color: tuple
    text: str
    txt_surface: pygame.Surface
    active: bool

    def __init__(self, x: int, y: int, w: int, h: int, font: pygame.font.Font, text: str = '') -> None:
        self.font = font
        self.blue = (148, 135, 199)
        self.black = (0, 0, 0)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.black
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> None:
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
            self.color = self.blue if self.active else self.black
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(
                    self.text, True, self.color)

    def update(self) -> None:
        """
        Updates the input box's width to fit the current text.
        """
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the input box and the current text on the specified screen.
        """
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class VirusSimulationApp:
    """
    A class to encapsulate the virus spread simulation application, including its UI elements and simulation logic.
    """
    screen: pygame.Surface
    clock: pygame.time.Clock
    font: pygame.font.Font
    white: tuple[int, int, int]
    button_color: tuple[int, int, int]
    house_density: str
    parameters: dict[str, Any]
    population_size: int
    population_size_box: InputBox
    input_text: str
    house_density_btn: Button
    initial_infected_count_slider: Slider
    infection_rate_slider: Slider
    incubation_period_slider: Slider
    death_rate_slider: Slider
    recovery_days_slider: Slider
    isolation_force_slider: Slider
    contact_density_slider: Slider
    start_simulation_button: Button

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 700))
        pygame.display.set_caption("Virus Spread Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.white = (255, 255, 255)
        self.button_color = (0, 120, 150)
        self.house_density = "MEDIUM"
        self.parameters = self.default_parameters()
        self.setup_ui_elements()

    def default_parameters(self) -> dict[str, Any]:
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
            'house_density': self.house_density,
            'contact_density': 5
        }

    def setup_ui_elements(self) -> None:
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
        self.population_size_box = InputBox(
            slider_start_x, 97, 200, 40, self.font)
        self.input_text = ''     # Variable to store the input text from the user

        # Button for changing house density
        # Allows users to cycle through house density.
        self.house_density_btn = Button(self.screen, slider_start_x, 448, 200, 40,
                                           text=f'{self.house_density}', fontSize=22, margin=20,
                                           inactiveColour=self.button_color, pressedColour=(0, 180, 180), radius=20)

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
        self.contact_density_slider = Slider(self.screen, slider_start_x, slider_start_y + 7 * slider_spacing,
                                             300, 10, min=1, max=10, step=1, initial=5)

        # Button for starting the simulation
        # This button triggers the fetching of parameters and potentially starts the simulation.
        self.start_simulation_button = Button(self.screen, 300, 580, 250, 50,
                                              text='Start Simulation', fontSize=30, margin=5,
                                              inactiveColour=self.button_color, pressedColour=(
                                                  100, 255, 100),
                                              radius=20, onClick=self.fetch_parameters)

    def toggle_house_density(self) -> None:
        """
        Toggles the house density status among predefined types.
        """
        if self.house_density == "LOW":
            self.house_density = "MEDIUM"
        elif self.house_density == "MEDIUM":
            self.house_density = "HIGH"
        else:
            self.house_density = "LOW"
        self.parameters['house_density'] = self.house_density
        self.house_density_btn.setText(self.house_density)

    def fetch_parameters(self) -> None:
        """
        Fetches simulation parameters from various UI elements and updates the global `parameters` dictionary.

        This function gathers user-defined values for the population size, initial infected count, infection rate,
        incubation period, death rate, recovery days, isolation force, and house density status from corresponding
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
        self.parameters['house_density'] = self.house_density
        self.parameters['contact_density'] = self.contact_density_slider.getValue()
        pygame.quit()  # Close the Pygame window to proceed with the simulation

    def run_simulation(self) -> "Simulation":
        """
        Initializes and runs the simulation based on the current configuration.

        This function creates instances of the `Virus` and `Policy` classes using the parameters
        specified in the global `parameters` dictionary. It then initializes a `Simulation` object
        with the population size, initial infected count, `Virus` instance, and `Policy` instance.

        The simulation environment is prepared by instantiating the necessary components with their
        respective parameters.
        """
        self.fetch_parameters()
        # print("Simulation parameters:", self.parameters)

        generate_graph(self.parameters)

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

        return sim

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
                    # Debugging: print the click position
                    print(f"Clicked at: {mouse_pos}")

                    # Check if the click is within the bounds of the 'Start Simulation' button
                    if 300 <= mouse_pos[0] <= 540 and 580 <= mouse_pos[1] <= 630:
                        self.population_size = int(self.population_size_box.text) \
                            if self.population_size_box.text.isdigit() else 500
                        self.run_simulation()  # Fetch simulation parameters from the UI
                        pygame.quit()
                        running = False
                        break

                    # Check if the click is within the bounds of the 'House Density' button
                    elif 327 <= mouse_pos[0] <= 524 and 450 <= mouse_pos[1] <= 486:
                        # Rotate through house density
                        self.toggle_house_density()

                self.population_size_box.handle_event(event)

            if not running:
                break

            # Clear the screen with a white background
            self.screen.fill(self.white)
            # Fetch and format the current values from sliders
            initial_infected_count_output = str(
                self.initial_infected_count_slider.getValue())
            infection_rate_output = str(
                round(self.infection_rate_slider.getValue() * 100)) + "%"
            incubation_period_output = str(
                self.incubation_period_slider.getValue())
            death_rate_output = str(
                round(self.death_rate_slider.getValue() * 100)) + "%"
            recovery_days_output = str(self.recovery_days_slider.getValue())
            isolation_force_output = str(
                round(self.isolation_force_slider.getValue() * 100)) + "%"
            contact_density_output = str(
                self.contact_density_slider.getValue())

            labels_and_values = [
                ('Population Size:', None),
                ('Initial Infected Count:', initial_infected_count_output),
                ('Infection Rate:', infection_rate_output),
                ('Incubation Period:', incubation_period_output),
                ('Death Rate:', death_rate_output),
                ('Recovery Days:', recovery_days_output),
                ('Isolation Force:', isolation_force_output),
                ('House Density:', None),
                ('Contact Density:', contact_density_output),
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
                self.contact_density_slider,
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

    def get_parameters(self) -> dict:
        """
        returns the parameters of current simulation
        """
        return self.parameters


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

    population_size: int
    graph: nx.Graph
    persons: dict[int, Person]
    virus: Virus
    policy: Policy

    def __init__(self, population_size: int, initial_infected_count: int, virus: Virus, policy: Policy) -> None:
        self.population_size = population_size
        self.graph = nx.Graph()
        self.persons = {i: Person() for i in range(population_size)}
        self.virus = virus
        self.policy = policy
        self.initial_infected(initial_infected_count)
        self.create_connections()

    def initial_infected(self, initial_infected_count: int) -> None:
        """
        Randomly selects a subset of the population to be initially infected with the virus.
        """
        infected_ids = random.sample(
            list(self.persons.keys()), initial_infected_count)
        for i in infected_ids:
            self.persons[i].status = "incubation"

    def create_connections(self) -> None:
        """
        Creates connections between individuals in the population to simulate their interactions.
        """
        return NotImplemented()

    def spread_virus(self) -> None:
        """
        Simulates the transmission of the virus between connected individuals based on the infection rate.
        """
        for person_id, person in self.persons.items():
            if person.status in ["incubation", "infected"]:
                for neighbor_id in self.graph.neighbors(person_id):
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
        return NotImplemented()


if __name__ == "__main__":

    import python_ta
    check_python_ta = False
    if check_python_ta:
        python_ta.check_all(config={
            'max-line-length': 120,
            'extra-imports': ["pygame", "pygame_widgets", "sys",
                            "matplotlib", "numpy", "networkx",
                              "pygame_widgets.slider", "pygame_widgets.textbox",
                              "typing_extensions", "simulation", "visualization",
                              "pygame_widgets.button", "random"],  # the names (strs) of imported modules
            # the names (strs) of functions that call print/open/input
            'allowed-io': [],
            # 'disabled': ["E9999"]
        })

    app = VirusSimulationApp()
    app.main_game_loop()
    # parameters = app.get_parameters()
    # print(parameters)
    # print("Y")
