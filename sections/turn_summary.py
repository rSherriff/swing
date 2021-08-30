from sections.section import Section

from ui.turn_summary_ui import TurnSummaryUI

class TurnSummary(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height)

        self.ui = TurnSummaryUI(self, x, y, self.tiles["graphic"])

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]
                
                count = 0
                for l in self.engine.turn_summary_text:
                    console.print(self.x + 2,self.y + 7 + count, l)
                    count += 1

            if self.ui is not None:
                self.ui.render(console)