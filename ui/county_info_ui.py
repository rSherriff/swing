from ui.ui import UI, Button, Tooltip

from actions.actions import AddActivity, RemoveActivity, UnlockCounty, EnactPolicy,OpenPolicyConfirmationDialog, OpenCountyConfirmationDialog
from verbs.activities import Activities, activity_templates
from verbs.policies import Policies, policy_templates


class LockedCountyInfoUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [4, 20, 16, 7]  # Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=OpenCountyConfirmationDialog(
                self.section.engine, "Unlock this county?", UnlockCounty( self.section.engine)), tiles=button_tiles)
        self.add_element(one_button)


class CountyInfoUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        startx = 20
        starty = 20
        ygap = 4
        count = 0
        for type in Activities:
            bd = [startx, starty + (count * ygap), 3, 3]  # Button Dimensions
            button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
            one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=RemoveActivity(
                self.section.engine, type), tiles=button_tiles)
            self.add_element(one_button)

            # Button Dimensions
            bd = [startx + 3, starty + (count * ygap), 3, 3]
            button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
            one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=AddActivity(
                self.section.engine, type), tiles=button_tiles)
            self.add_element(one_button)

            td = [startx, starty + (count * ygap)]
            tooltip = Tooltip(x=td[0], y=td[1], width=7, height=3, x_offset=-1,
                              y_offset=2, text=activity_templates[type].description)
            self.add_element(tooltip)

            count += 1

        startx = 42
        starty = 21
        ygap = 5
        count = 0
        for type in Policies:
            bd = [startx, starty + (count * ygap), 3, 3]  # Button Dimensions
            button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
            one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=OpenPolicyConfirmationDialog(
                self.section.engine, "Enact this policy?", type, EnactPolicy(self.section.engine, type)), tiles=button_tiles)
            self.add_element(one_button)

            td = [startx, starty + (count * ygap)]
            tooltip = Tooltip(x=td[0], y=td[1], width=3, height=3, x_offset=-15,
                              y_offset=2, text=policy_templates[type].description)
            self.add_element(tooltip)

            count += 1
