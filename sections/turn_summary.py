from sections.section import Section

from ui.turn_summary_ui import TurnSummaryUI

class TurnSummary(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height, "turn_summary.xp")

        self.ui = TurnSummaryUI(self, x, y, self.tiles["graphic"])

        self.start_x = self.x + 7
        self.start_y = self.y + 8

        self.power_x = self.x + 24
        self.support_x = self.x + 35

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]
                
                count = 0
                for l in self.engine.turn_summary_text:
                    console.print(self.start_x,self.start_y + count, l[0])
                    console.print(self.power_x,self.start_y + count, str(l[1]))
                    console.print(self.support_x,self.start_y + count, str(l[2]))
                    count += 3

            if self.ui is not None:
                self.ui.render(console)
