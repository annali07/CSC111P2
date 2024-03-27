class Virus:
    """ Virus Class
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
