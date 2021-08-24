from sections.section import Section
from ui.county_info_ui import LockedCountyInfoUI, CountyInfoUI

class CountyInfo(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):

        self.name_point = (x, y)
        self.unlock_text_point = (x, y+1)
        super().__init__(engine, x, y, width, height)

        
        self.unlockedUI = CountyInfoUI(self, x, y, self.tiles["graphic"])
        self.lockedUI = LockedCountyInfoUI(self, x, y, self.tiles["graphic"])
        self.ui = self.lockedUI

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

        county = self.engine.county_manager.get_selected_county()
        if county is not None:
            console.print(self.name_point[0], self.name_point[1], county.name)

            if county.unlocked:
                self.ui = self.unlockedUI
                self.ui.render(console)
            elif not county.unlocked:
                self.ui = self.lockedUI
                console.print(self.unlock_text_point[0], self.unlock_text_point[1], "Unlock County for " + str(county.unlock_cost) + " power points.")
                self.ui.render(console)