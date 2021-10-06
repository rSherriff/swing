import gzip
import random
from typing import TYPE_CHECKING, Iterator, Tuple

import numpy as np
import tcod
import tile_types
import xp_loader
from ui.map_ui import MapUI
from voronoi import Voronoi

from sections.section import Section

GRASS_GREEN = (17, 41, 6)
DARK_GREEN = (40, 50, 6)
DRY_MUD_BROWN = (75, 57, 35)
DRY_MUD_BROWN_B = (75, 65, 35)
WET_MUD_BROWN = (39, 27, 10)

class Map(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        #super().__init__(engine, x, y, width, height, "map.xp")

        self.engine = engine

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        tile = tile_types.background_tile
        tile["graphic"]["bg"] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.tiles =  np.full((self.width, self.height), fill_value=tile, order="F")
        self.ui = None

        xp_file = gzip.open("images/" + 'map.xp')
        raw_data = xp_file.read()
        xp_file.close()

        self.generate_landscape(self.engine, self.tiles)
    
        xp_data = xp_loader.load_xp_string(raw_data)
        for h in range(0, self.height):
            if h < xp_data['height']:
                for w in range(0, self.width):
                    if w < xp_data['width']:
                        if xp_data['layer_data'][1]['cells'][w][h][0] == ord('#'):
                            self.tiles[w, h]['graphic']["fg"] = xp_data['layer_data'][0]['cells'][w][h][1]
                            self.tiles[w, h]['graphic']["ch"] = xp_data['layer_data'][0]['cells'][w][h][0]                            
                            self.tiles[w, h]['graphic']["bg"] = xp_data['layer_data'][0]['cells'][w][h][2]
                        elif xp_data['layer_data'][0]['cells'][w][h][1] == (255,255,255):
                            self.tiles[w, h]['graphic']["fg"] = (128,128,128)
                            self.tiles[w, h]['graphic']["ch"] = xp_data['layer_data'][0]['cells'][w][h][0]
                            
                    else:
                        break
            else:
                break
        

        self.invisible = False
        self.ui = MapUI(self, x, y, self.tiles["graphic"])

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]
                pass

            if self.ui is not None:
                self.ui.render(console)


    def generate_landscape(self, engine, landscape):

        map_center = (int(self.width / 2), int(self.height / 2))

        # Generate and draw a voronoi diagram, then grab the points from a few of its sections to fill later
        vorgen = Voronoi(40, np.array([-1, self.width + 1, -1, self.height + 1]))
        self.draw_voronoi(vorgen, landscape, (255,255,255))
        voronoi_fill_points = self.get_voronoi_fill_points(num_regions=3, vorgen=vorgen, landscape=landscape)

        self.clear_landscape(landscape, GRASS_GREEN, DARK_GREEN)

        noise = tcod.noise.Noise(
            dimensions=2,
            algorithm=tcod.NOISE_PERLIN,
            implementation=tcod.noise.TURBULENCE,
            hurst=0.5,
            lacunarity=5.0,
            octaves=2,
            seed=None,
        )

        # Add a base layer of smooth, gradually changing noise to form base layer
        self.add_smooth_noise_to_landscape(landscape, noise, 0.05, GRASS_GREEN, DARK_GREEN)

        # Shade the voronoi sections we grabbed before now we have our base layer down
        self.fill_regions(landscape, voronoi_fill_points, DRY_MUD_BROWN, WET_MUD_BROWN, DARK_GREEN, DRY_MUD_BROWN_B)

        # Add more granular noise on top to break things up
        self.add_noise_to_landscape(landscape, noise, 0.9, GRASS_GREEN, DARK_GREEN)


    def clear_landscape(self,landscape, bg_colour, fg_colour):
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.tiles[x, y]["graphic"]["bg"] = bg_colour
                self.tiles[x, y]["graphic"]["ch"] = 9617
                self.tiles[x, y]["graphic"]["fg"] = self.colour_lerp(bg_colour, fg_colour, random.random())


    def draw_voronoi(self,vorgen, landscape, colour):
        for region in vorgen.vor.filtered_regions:
            vertices = vorgen.vor.vertices[region, :]
            for i in range(0, len(vertices)):
                nextVertex = i + 1
                if(i == len(vertices) - 1):
                    nextVertex = 0
                for x, y in self.line_between((int(vertices[i][0]), int(vertices[i][1])), (int(vertices[nextVertex][0]), int(vertices[nextVertex][1]))):
                    if x >= 0 and y >= 0 and x < self.width and y < self.height:
                        self.tiles[x, y]["graphic"]["bg"] = colour


    def get_voronoi_fill_points(self,num_regions, vorgen, landscape):
        dirt_patch_points = list()
        for i in range(0, num_regions):
            point = vorgen.vor.filtered_points[i]
            dirt_patch_points += [self.get_fill_points(landscape, point)]

        return dirt_patch_points


    def fill_regions(self,landscape, region_points, start_colour, end_colour, blend_colour, accent_colour):
        # Start colour, end colour - The range of colours you want this tile to become
        # Blend colour - the colour this section blends into, tiles on the edge of the section will completely fade into it
        # accent colour - an extra dash for tiles that are completly surrounded by similar coloured tiles
        for i in region_points:
            for point in i:
                landscape[point[0], point[1]]["graphic"]["bg"] = start_colour

        for i in region_points:
            for point in i:
                x, y = point[0], point[1]
                score = 0
                if (x - 1, y) in i:
                    score += 1
                if (x + 1, y) in i:
                    score += 1
                if (x, y - 1) in i:
                    score += 1
                if (x, y + 1) in i:
                    score += 1
                if (x - 1, y + 1) in i:
                    score += 1
                if (x + 1, y + 1) in i:
                    score += 1
                if (x + 1, y - 1) in i:
                    score += 1
                if (x + 1, y + 1) in i:
                    score += 1

                if random.random() < 0.5:
                    landscape[x, y]["graphic"]["ch"] = 9617
                    landscape[x, y]["graphic"]["fg"] = self.colour_lerp(start_colour, end_colour, min(0.4, random.random()))

                landscape[x, y]["graphic"]["bg"] = self.colour_lerp(blend_colour, start_colour, score / 8)

                if score is 8:
                    landscape[x, y]["graphic"]["bg"] = self.colour_lerp(landscape[x, y]["graphic"]["bg"], accent_colour, random.random())


    def add_smooth_noise_to_landscape(self,landscape, noise, scale, start_colour, end_colour):
        # Create an open multi-dimensional mesh-grid.
        ogrid = [np.arange(self.width, dtype=np.float32),
                np.arange(self.height, dtype=np.float32)]

        ogrid[0] *= scale
        ogrid[1] *= scale

        # Return the sampled noise from this grid of points.
        samples = noise.sample_ogrid(ogrid)

        for x in range(0, self.width):
            for y in range(0, self.height):
                landscape[x, y]["graphic"]["bg"] = self.colour_lerp(landscape[x, y]["graphic"]["bg"], end_colour, samples[x, y] / 1.2)


    def add_noise_to_landscape(self,landscape, noise, threshold, start_colour, end_colour):
        # Create an open multi-dimensional mesh-grid.
        ogrid = [np.arange(self.width, dtype=np.float32),
                np.arange(self.height, dtype=np.float32)]

        # Return the sampled noise from this grid of points.
        samples = noise.sample_ogrid(ogrid)
        for x in range(0, self.width):
            for y in range(0, self.height):
                if samples[x, y] > threshold:
                    old_range = (1 - threshold)
                    new_value = ((samples[x, y] - threshold) / old_range)
                    colour = self.colour_lerp(start_colour, end_colour, max(0.5, random.random()))
                    landscape[x, y]["graphic"]["ch"] = 9617
                    landscape[x, y]["graphic"]["bg"] = colour
                    landscape[x, y]["graphic"]["fg"] = self.colour_lerp(colour, DARK_GREEN, max(0.8, random.random()))


    def line_between(self,
        start: Tuple[int, int], end: Tuple[int, int]
    ) -> Iterator[Tuple[int, int]]:
        """Return an L-shaped tunnel between these two points."""
        x1, y1 = start
        x2, y2 = end

        # Generate the coordinates for this tunnel.
        for x, y in tcod.los.bresenham((x1, y1), (x2, y2)).tolist():
            yield x, y


    def get_fill_points(self,landscape, start_coords: Tuple[int, int]):
        orig_value = (landscape[start_coords[0], start_coords[1]]["graphic"]["bg"]).copy()

        stack = set(((start_coords[0], start_coords[1]),))
        points = list()
        while stack:
            x, y = stack.pop()
            res = all(i == j for i, j in zip(landscape[x, y]["graphic"]["bg"], orig_value))
            if res:
                landscape[x, y]["graphic"]["bg"] = (255 - orig_value[0], 255 - orig_value[1], 255 - orig_value[2])
                points.append((x, y))
                if x > 0:
                    stack.add((x - 1, y))
                if x < (self.width - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (self.height - 1):
                    stack.add((x, y + 1))

        return points


    def get_surrounding_tiles(self,position: Tuple[int, int]):
        return ([position[0] - 1, position[1] - 1],
                [position[0] - 1, position[1] + 1],
                [position[0] + 1, position[1] - 1],
                [position[0] + 1, position[1] + 1],
                [position[0] - 1, position[1]],
                [position[0] + 1, position[1]],
                [position[0], position[1] - 1],
                [position[0], position[1] + 1],
                )


    def colour_lerp(self,colour1: Tuple[int, int, int], colour2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        return (int(colour1[0] + t * (colour2[0] - colour1[0])), int(colour1[1] + t * (colour2[1] - colour1[1])), int(colour1[2] + t * (colour2[2] - colour1[2])))
