from ui.ui import UI
from ui.ui import Button

from actions.actions import SelectCounty

class MapUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [4, 1,10,5] #Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Kent'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [15, 1,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Surrey'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [26, 1,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Sussex'), tiles=button_tiles )
        self.add_element(one_button)