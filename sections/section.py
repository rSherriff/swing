import numpy as np
import xp_loader
import gzip
import tile_types
import random

class Section:
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        self.engine = engine

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        tile = tile_types.background_tile
        tile["graphic"]["bg"] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.tiles =  np.full((self.width, self.height), fill_value=tile, order="F")
        self.ui = None

        if xp_filepath:
            xp_file = gzip.open("images/" + xp_filepath)
            raw_data = xp_file.read()
            xp_file.close()

            xp_data = xp_loader.load_xp_string(raw_data)
            for h in range(0, self.height):
                if h < xp_data['height']:
                    for w in range(0, self.width):
                        if w < xp_data['width']:
                            self.tiles[w, h]['graphic'] = xp_data['layer_data'][0]['cells'][w][h]
                        else:
                            break
                else:
                    break

        self.invisible = False

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

            if self.ui is not None:
                self.ui.render(console)

    def update(self):
        pass