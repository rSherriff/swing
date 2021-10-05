from sections.section import Section

from ui.activities_bar_ui import ActivitiesBarUI

class ActivitiesBar(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height, "action_bar.xp")

        self.ui = ActivitiesBarUI(self, x, y, self.tiles["graphic"])