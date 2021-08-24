from counties.county import County

from verbs.activities import Activities

class CountyManager():
    def __init__(self):
        self.counties = {}
        self.selected_county = ""

    def create_counties(self):
        kent = County()
        kent.name = "Kent"
        kent.unlocked = True
        self.counties[kent.name] = kent

        sussex = County()
        sussex.name = "Sussex"
        sussex.unlock_cost = 100
        self.counties[sussex.name] = sussex

        surrey = County()
        surrey.name = "Surrey"
        surrey.unlock_cost = 500
        self.counties[surrey.name] = surrey

    def get_county(self, name):
        if name in self.counties:
            return self.counties[name]
        else:
            return None

    def get_selected_county(self):
        return self.get_county(self.selected_county)

    def add_activity(self, type):
        self.get_selected_county().add_activity(type)

    def remove_activity(self, type):
        return self.get_selected_county().remove_activity(type)

    def process_all_activites(self):
        effects = {}
        for county in self.counties.values():
            effects[county.name] = county.process_activities()

        return effects

    def unlock_selected_county(self):
        self.get_selected_county().unlocked = True

    def enact_policy(self, type):
        self.get_selected_county().enact_policy(type)

    
