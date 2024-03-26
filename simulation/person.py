

class Person:
    def __init__(self, status="uninfected"):
        self.status = status    # Can be "uninfected", "incubation", or "infected"
        self.days_infected = 0  # Track the number of days since infection

    def update_status(self):
        # Status from incubation to infected
        if self.status == "incubation" and self.days_infected >= Virus.incubation_period:
            self.status = "infected"
        # Already infected -> Undating the date of infection
        elif self.status == "infected":
            self.days_infected += 1
