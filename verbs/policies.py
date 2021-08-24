from enum import Enum, auto


class Policies(Enum):
    INCREASE_WAGES = auto()
    BAN_MACHINES = auto()
    RENT_DECREASE = auto()
    TITHE_DECREASE = auto()

class Policy():
    def __init__(self, type, cost) -> None:
        self.type = type
        self.cost = cost

policies = {}
policies[Policies.INCREASE_WAGES] = Policy(Policies.INCREASE_WAGES, 100)
policies[Policies.BAN_MACHINES] = Policy(Policies.BAN_MACHINES, 100)
policies[Policies.RENT_DECREASE] = Policy(Policies.RENT_DECREASE, 100)
policies[Policies.TITHE_DECREASE] = Policy(Policies.TITHE_DECREASE, 100)
