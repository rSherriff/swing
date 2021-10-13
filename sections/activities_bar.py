from sections.section import Section

from ui.activities_bar_ui import ActivitiesBarUI

class ActivitiesBar(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height, "action_bar.xp")

        self.ui = ActivitiesBarUI(self, x, y, self.tiles["graphic"])
        self.power_x = self.x + 14
        self.power_y = self.y + 2
        self.support_x = self.x + 60
        self.support_y = self.y + 2

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

                power_string =''
                if self.engine.power < -1000:
                    power_string = f"{self.engine.power:05d}"   
                else:
                    power_string = f"{self.engine.power:04d}"   
                count = 0
                for char in power_string:
                    console.tiles_rgb[self.power_x + (count * 3) + (count * 1): self.power_x +(count * 3)+ 3 + (count * 1), self.power_y: self.power_y + 6]["ch"] = self.engine.fontmanager.get_font("number_font").get_character(char)["ch"]
                    console.tiles_rgb[self.power_x + (count * 3) + (count * 1): self.power_x +(count * 3)+ 3 + (count * 1), self.power_y: self.power_y + 6]["fg"] = self.engine.fontmanager.get_font("number_font").get_character(char)["fg"]
                    count += 1

                support_string =''
                if self.engine.support < -1000:
                    support_string = f"{self.engine.support:05d}"   
                else:
                    support_string = f"{self.engine.support:04d}"   
                count = 0
                for char in support_string:
                    console.tiles_rgb[self.support_x + (count * 3) + (count * 1): self.support_x +(count * 3)+ 3 + (count * 1), self.support_y: self.support_y + 6]["ch"] = self.engine.fontmanager.get_font("number_font").get_character(char)["ch"]
                    console.tiles_rgb[self.support_x + (count * 3) + (count * 1): self.support_x +(count * 3)+ 3 + (count * 1), self.support_y: self.support_y + 6]["fg"] = self.engine.fontmanager.get_font("number_font").get_character(char)["fg"]
                    count += 1

            if self.ui is not None:
                self.ui.render(console)

    
 