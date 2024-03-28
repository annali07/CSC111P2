from __future__ import annotations
import virus
import policy


class Person:
    """ Person Class
    """
    relationship: set[Person]
    status: str     # uninfected/incubation/infected/dead/recovered
    days_infected: int

    def __init__(self) -> None:
        self.status = "uninfected"
        self.days_infected = 0
        self.relationship = set()

    def add_connection(self, other_person: Person) -> None:
        """Add a bidirectional connection with another person.
        """
        if other_person not in self.relationship:
            self.relationship.append(other_person)
            other_person.relationship.append(self)

    def update_status(self, virus: Virus) -> None:
        """The method for updating the status of individuals based on the current status and other variables
        """
        if self.status == "incubation":
            if self.days_infected >= virus.incubation_period:
                self.status = "infected"
                self.days_infected = 0
            else:
                self.days_infected += 1

        elif self.status == "infected":
            self.days_infected += 1
            if self.days_infected >= virus.recovery_days:
                if random.random() < virus.death_rate:      # First version
                    self.status = "dead"
                else:
                    self.status = "recovered"

        elif self.status in ["recovered", "dead"]:
            pass
