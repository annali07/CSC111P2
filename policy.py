from person import Person
from virus import Virus


class Policy:
    """ Policy Class
    """
    isolate_infected: bool
    clear_neighbors: bool

    def __init__(self, isolate_infected: bool, clear_neighbors: bool) -> None:
        self.isolate_infected = isolate_infected
        self.clear_neighbors = clear_neighbors

    def enforce_policy(self):
        """Modify the graph or individual statuses based on the policy
        For example, removing connections (edges) if individuals are isolated
        """
        pass
