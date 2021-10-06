
from ui.county_info_ui import CountyInfoUI, LockedCountyInfoUI
from verbs.activities import Activities, activity_templates
from verbs.policies import Policies, policy_templates

from sections.section import Section


class CountyInfo(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height, "county_info.xp")

        self.name_point = (x + 1, y + 1)
        self.unlock_text_point = (x + 2, y+11)        

        self.unlockedUI = CountyInfoUI(self, x, y, self.tiles["graphic"])
        self.lockedUI = LockedCountyInfoUI(self, x, y, self.tiles["graphic"])
        self.ui = self.lockedUI

        self.info_x = self.x + 1
        self.info_y = self.y + 3

        self.activity_buttons_x = self.x + 2
        self.activity_buttons_y = self.y + 20
        self.activity_buttons_y_gap = 4

        self.policy_buttons_x = self.x + 27
        self.policy_buttons_y = self.y + 20
        self.policy_buttons_y_gap = 5

        self.flag_x = self.x + 25
        self.flag_y = self.y + 3

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

        county = self.engine.county_manager.get_selected_county()
    
        if county is not None:
            console.print(self.name_point[0], self.name_point[1], county.name,  (255,255,255))

            console.print(self.info_x, self.info_y,     " Avg. Wages: " + str(county.wage), (255,255,255))
            console.print(self.info_x, self.info_y + 2, " Avg. Tithes: " + str(county.tithes),  (255,255,255))
            console.print(self.info_x, self.info_y + 4, " Avg. Rent: " + str(county.rent),  (255,255,255))
            console.print(self.info_x, self.info_y + 6, " Percentage Cereal: " + str(county.cereal_percent),  (255,255,255))

            console.tiles_rgb[self.flag_x : self.flag_x + county.flag_width, self.flag_y: self.flag_y + county.flag_height] = county.flag_image.tiles["graphic"]

            if not county.unlocked:
                self.ui = self.lockedUI
                console.print(self.unlock_text_point[0], self.unlock_text_point[1], "Unlock County: ",  (255,255,255))
                console.print(self.unlock_text_point[0], self.unlock_text_point[1] + 1, "   " + str(county.unlock_cost) + " power points.",  (255,255,255))
                self.ui.render(console)
            elif county.unlocked:
                self.ui = self.unlockedUI

                console.print(self.activity_buttons_x, self.activity_buttons_y - 3, "Activity Points:" + str(self.engine.activity_points),  (255,255,255))
                count = 0
                for a in Activities:
                    console.print(self.activity_buttons_x, self.activity_buttons_y + (count * self.activity_buttons_y_gap), activity_templates[a].name,  (255,255,255))
                    console.print(self.activity_buttons_x, self.activity_buttons_y + (count * self.activity_buttons_y_gap) + 2, "< - - - - - - >",  (255,255,255))
                    console.print(self.activity_buttons_x + (county.get_num_activity(a) *2)+ 2, self.activity_buttons_y + (count * self.activity_buttons_y_gap) + 2, "O",  (255,255,255))
                    console.print(self.activity_buttons_x + 15, self.activity_buttons_y + (count * self.activity_buttons_y_gap) + 2, "x" + str(county.get_num_activity(a)),  (255,255,255))
                    count += 1

                count = 0
                for p in Policies:
                    console.print(self.policy_buttons_x, self.policy_buttons_y + (count * self.policy_buttons_y_gap), policy_templates[p].name,  (255,255,255))
                    if county.is_policy_enacted(p):
                        console.print(self.policy_buttons_x + 3, self.policy_buttons_y + (count * self.policy_buttons_y_gap) + 2, "Enacted!",  (255,255,255))
                    count += 1

                self.ui.render(console)
