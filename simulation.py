"""
The purpose of this document is to outline possible further enhancement for encapsulating
data needed to run the simulation. This way, faster and more efficient comparisons can be
made when studying specific virus and policies proposed by governments.
"""

from __future__ import annotations
import random


class Virus:
    """
    Represents a virus in a simulation of an infectious disease outbreak.

    Attributes:
        incubation_period (int): The period in days between exposure to the virus
            and the onset of symptoms.
        infection_rate (float): The probability of the virus being transmitted
            between two connected individuals per day.
        death_rate (float): The probability of an infected individual dying from
            the virus once the recovery period has passed.
        recovery_days (int): The number of days it takes for an infected individual
            to either recover or die from the virus.
    """

    incubation_period: int
    infection_rate: float
    death_rate: float
    recovery_days: int

    def __init__(self, incubation_period: int, infection_rate: float, death_rate: float, recovery_days: int) -> None:
        self.incubation_period = incubation_period
        self.infection_rate = infection_rate
        self.death_rate = death_rate
        self.recovery_days = recovery_days      # Period ultil recovery or death


class Person:
    """
    Represents an individual in a simulation of an infectious disease outbreak.

    Attributes:
        relationship (Set[Person]): A set of other Person instances to which this individual is connected,
                                    representing potential pathways for virus transmission.
        status (str): The current health status of the individual, which can be 'uninfected', 'incubation',
                      'infected', 'dead', or 'recovered'.
        days_infected (int): The number of days the individual has been infected, used to track progression through
                             incubation and infectious periods.
    """

    status: str
    days_infected: int
    relationship: set

    def __init__(self) -> None:
        self.status = "uninfected"  # Initial health status is 'uninfected'
        self.days_infected = 0      # Initially, the individual has not been infected
        self.relationship = set()   # Initializes an empty set for relationships

    def add_connection(self, other_person: 'Person') -> None:
        """
        Adds a bidirectional connection between this person and another, representing a potential pathway for virus
        transmission.
        """
        # Ensure the connection is bidirectional and doesn't duplicate
        if other_person not in self.relationship:
            # Adding a connection from this person to the other
            self.relationship.add(other_person)
            # Ensuring the connection is reciprocal
            other_person.relationship.add(self)

    def update_status(self, virus: 'Virus') -> None:
        """
        Updates the individual's health status based on the current status, virus 
        characteristics, and the passage of time.
        """
        if self.status == "incubation":
            self.days_infected += 1
            if self.days_infected >= virus.incubation_period:
                self.status = "infected"
                self.days_infected = 0  # Reset days infected upon entering the 'infected' state

            # If 'infected', determine if the person recovers or dies after the infectious period
        elif self.status == "infected":
            self.days_infected += 1
            if self.days_infected >= virus.recovery_days:
                self.status = "dead" if random.random() < virus.death_rate else "recovered"

            # No action needed if the person is already 'recovered' or 'dead'
        elif self.status in ["recovered", "dead"]:
            pass


class Policy:
    """
    Represents a health policy or intervention strategy in a disease outbreak simulation.

    This class models the effects of various policy decisions, such as social distancing or quarantine measures, on the
    spread of the virus within the population.

    Attributes:
        isolate_force (float): A measure of the stringency and effectiveness of isolation policies.
    """

    isolate_force: float

    def __init__(self, isolate_force: float) -> None:
        self.isolate_force = isolate_force

    def enforce_policy(self) -> None:
        """
        Applies the policy's effects to the simulation.
        """
        return NotImplemented


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
            'allowed-io': [],
            # 'disabled': ["E9999"]
        })
