from counties.county import County

from activities import Activities

class CountyManager():
    def __init__(self):
        self.counties = {}
        self.selected_county = ""

    def create_counties(self):
        kent = County()
        kent.name = "Kent"
        self.counties[kent.name] = kent

        sussex = County()
        sussex.name = "Sussex"
        self.counties[sussex.name] = sussex

        surrey = County()
        surrey.name = "Surrey"
        self.counties[surrey.name] = surrey

    def get_county(self, name):
        if name in self.counties:
            return self.counties[name]
        else:
            return None

    def get_selected_county(self):
        return self.get_county(self.selected_county)

    def process_activity(self, type, pow, sup):
        return pow, sup
