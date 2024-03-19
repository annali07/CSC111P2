class Graph:
    def __init__(self):
        self._vertices = {}  # Key: person_id, Value: Person object
        self._edges = []  # List of tuples representing edges between vertices

    def add_person(self, person_id, person):
        """"""
        self._vertices[person_id] = person

    def add_connection(self, person_id1, person_id2):
        """"""
        self._edges.append((person_id1, person_id2))

    def spread_virus(self):
        """Implement logic to spread the virus based on current graph structure and virus characteristics
        """
        pass

    def apply_policy(self, policy):
        """Implement logic to apply government policies
        """
        pass
