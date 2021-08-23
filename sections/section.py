import numpy as np
import tile_types
import random

class Section:
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        self.engine = engine

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        tile = tile_types.background_tile
        tile["graphic"]["bg"] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.tiles =  np.full((width, height), fill_value=tile, order="F")
        self.ui = None

        self.invisible = False

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

            if self.ui is not None:
                self.ui.render(console)

    def update(self):
        pass