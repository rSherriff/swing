import json

from verbs.activities import Activities

from counties.county import County


class CountyManager():
    def __init__(self):
        self.counties = {}
        self.selected_county = ""
        with open ( "data/counties.json" ) as f:
            data = json.load(f)
            for c in data["counties"]:
                county = County()
                county.name = c["name"]
                county.unlock_cost = c["unlock_cost"]
                county.unlocked = c["unlocked"]
                county.wage = c["wage"]
                county.rent = c["rent"]
                county.tithes = c["tithes"]
                county.load_flag("images/" + c["flag"] + ".xp")

                self.counties[county.name] = county

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

    
