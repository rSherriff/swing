from ui.ui import UI, Button, Tooltip

from actions.actions import AdvanceTurn, OpenConfirmationDialog


class ActivitiesBarUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [106, 2, 13, 6]  # Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=OpenConfirmationDialog(
            self.section.engine, "Advance the game?", AdvanceTurn(self.section.engine)), tiles=button_tiles)
        self.add_element(one_button)

        td = [106, 2]
        tooltip = Tooltip(x=td[0], y=td[1], width=10, height=5,
                          x_offset=-1, y_offset=2, text="Advance the game.")
        self.add_element(tooltip)
