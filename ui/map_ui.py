from ui.ui import UI
from ui.ui import Button, ShapedButton

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
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Sussex'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [26, 1,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Surrey'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [37, 1,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Berkshire'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [4, 7,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Hampshire'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [15, 7,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Wiltshire'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [26, 7,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Buckinghamshire'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [37, 7,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Hertfordshire'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [4, 13,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Bedfordshire'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [15, 13,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Dorset'), tiles=button_tiles )
        self.add_element(one_button)

        bd = [26, 13,10,5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        shaped_button_tiles = ((1,1),(2,1))
        one_button = ShapedButton(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=SelectCounty(self.section.engine, 'Dorset'), tiles=button_tiles, active_tiles=shaped_button_tiles )
        self.add_element(one_button)