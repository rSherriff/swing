from ui.ui import UI, Button, Tooltip

from actions.actions import CloseTurnSummary

class TurnSummaryUI(UI):
    def __init__(self, section, x, y, tiles):
        super().__init__(section, x, y)
        self.elements = list()
        
        bd = [49, 36,14,5] #Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        one_button = Button(x=bd[0], y=bd[1], width=bd[2], height=bd[3], click_action=CloseTurnSummary(self.section.engine), tiles=button_tiles )
        self.add_element(one_button)
    