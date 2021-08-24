
from typing import Tuple
from verbs.activities import Activities
from verbs.policies import Policies

class County():
    def __init__(self):
        self.name = ""
        self.unlock_cost = 0
        self.unlocked = False
        self.activities = {}
        self.max_activity = 5

        self.wage = 0
        self.tithes = 0
        self.rent = 0
        self.cereal_percent = 0

        self.policies = {}
        for p in Policies:
            self.policies[p] = False


    def add_activity(self, type):
        if type in self.activities:
            self.activities[type] = min(self.activities[type] + 1, self.max_activity)
        else:
            self.activities[type] = 1

        print("Added " + str(type) + " to " + self.name + ", total: " +  str(self.activities[type]))

    def remove_activity(self, type):
        if type in self.activities and self.activities[type] > 0:
            self.activities[type] = max(self.activities[type] - 1, 0)
            print("Removed " + str(type) + " from " + self.name + ", remaining: " + str( self.activities[type]))
            return True
        else:
            print("Attempting to remove " + str(type) + " from " + self.name + ", but it doesn't exist!")
            return False


    def process_activities(self):
        pow = sup = 0
        for a, t in self.activities.items():
            for i in range(t):
                print("Processing " + str(a) + " in " + self.name)
                if a is Activities.BREAKING:
                    pow += 10
                    sup += 10
                elif a is Activities.ARSON:
                    pow += 20
                    sup += -30
                elif a is Activities.LETTER:
                    pow += 20
                    sup += -10
                elif a is Activities.MEETING:
                    pow += -10
                    sup += 20
                elif a is Activities.ROBBERY:
                    pow += 10
                    sup += -10

        self.activities.clear()
        return pow, sup

    def enact_policy(self, type):
        self.policies[type] = True
        print("Enacted " + str(type) + " in " + self.name)

