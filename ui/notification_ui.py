from ui.ui import UI, Button, Tooltip

from actions.actions import AdvanceTurn, CloseNotificationDialog
from verbs.activities import Activities


class NotificationUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()

        bd = [23, 3, 14, 5]
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        close_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=CloseNotificationDialog(
            self.section.engine), tiles=button_tiles)
        self.add_element(close_button)

    def reset(self, confirmation_action):
        self.elements[0].set_action(confirmation_action)
