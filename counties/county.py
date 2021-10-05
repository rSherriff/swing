
from typing import Tuple
from verbs.activities import Activities, Activity, activity_templates
from verbs.policies import Policies
from tcod import Console
from image import Image

class County():
    def __init__(self):
        self.name = ""
        self.unlock_cost = 0
        self.unlocked = False
        self.activities = {}
        self.max_activity = 5

        self.flag_width = 20
        self.flag_height = 10

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

    def get_num_activity(self, type):
        if type in self.activities:
            return self.activities[type]
        else:
            return 0

    def process_activities(self):
        pow = sup = 0
        for a, t in self.activities.items():
            for i in range(t):
                print("Processing " + str(a) + " in " + self.name)
                if a is Activities.BREAKING:
                    pow += activity_templates[Activities.BREAKING].power
                    sup += activity_templates[Activities.BREAKING].support
                elif a is Activities.ARSON:
                    pow += activity_templates[Activities.ARSON].power
                    sup += activity_templates[Activities.ARSON].support
                elif a is Activities.LETTER:
                    pow += activity_templates[Activities.LETTER].power
                    sup += activity_templates[Activities.LETTER].support
                elif a is Activities.MEETING:
                    pow += activity_templates[Activities.MEETING].power
                    sup += activity_templates[Activities.MEETING].support
                elif a is Activities.ROBBERY:
                    pow += activity_templates[Activities.ROBBERY].power
                    sup += activity_templates[Activities.ROBBERY].support

        self.activities.clear()
        return pow, sup

    def enact_policy(self, type):
        self.policies[type] = True
        print("Enacted " + str(type) + " in " + self.name)

    def is_policy_enacted(self, type):
        if type in self.policies:
            return self.policies[type]
        else:
            return False
            
    def load_flag(self, flag_file):
        self.flag_image = Image(20,10, flag_file)

    def get_flag(self):
        temp_console = Console(width=self.flag_width, height=self.flag_height, order="F")

        for h in range(0,self.flag_height):
            for w in range(0, self.flag_width):
                temp_console.tiles_rgb[w,h][2] = (0,255,0)

        return temp_console

