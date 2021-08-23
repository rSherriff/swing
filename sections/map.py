from sections.section import Section

from ui.map_ui import MapUI

class Map(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height)

        self.ui = MapUI(self, x, y, self.tiles["graphic"])