from ui.ui import UI, Button

from actions.actions import AddActivity, RemoveActivity, UnlockCounty, EnactPolicy
from verbs.activities import Activities
from verbs.policies import Policies

class LockedCountyInfoUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [4, 1,10,5] #Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=UnlockCounty(self.section.engine), tiles=button_tiles )
        self.add_element(one_button)

class CountyInfoUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        startx = 10
        starty = 20
        ygap = 3
        count = 0
        for type in Activities:
            bd = [startx, starty +(count * ygap),2,2] #Button Dimensions
            button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
            one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=RemoveActivity(self.section.engine, type), tiles=button_tiles )
            self.add_element(one_button)

            bd = [startx + 3, starty +(count * ygap),2,2] #Button Dimensions
            button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
            one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=AddActivity(self.section.engine, type), tiles=button_tiles )
            self.add_element(one_button)

            count += 1
        
        startx = 20
        starty = 20
        ygap = 3
        count = 0
        for type in Policies:
            bd = [startx, starty +(count * ygap),2,2] #Button Dimensions
            button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
            one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=EnactPolicy(self.section.engine, type), tiles=button_tiles )
            self.add_element(one_button)

            count += 1

        