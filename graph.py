from person import Person
from virus import Virus
from policy import Policy


class Graph:
    """ Graph Class
    """

    def __init__(self) -> None:
        self._vertices = {}  # Key: person_id, Value: Person object

    def add_person(self, person_id: int, person: Person) -> None:
        """This method will create the dict for a person
        """
        self._vertices[person_id] = person

    def add_connection(self, person_id1: int, person_id2: int) -> None:
        """This method will connect two persons in the network
        """
        self._edges.append((person_id1, person_id2))

    def spread_virus(self) -> None:
        """Implement logic to spread the virus based on current graph structure and virus characteristics
        """
        pass

    def apply_policy(self, policy: Policy) -> None:
        """Implement logic to apply government policies
        """
        pass
