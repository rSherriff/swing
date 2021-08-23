from sections.section import Section

class CountyInfo(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):

        self.name_point = (x, y)
        super().__init__(engine, x, y, width, height)

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

            if self.ui is not None:
                self.ui.render(console)

        county = self.engine.county_manager.get_selected_county()
        if county is not None:
            console.print(self.name_point[0], self.name_point[1], county.name)