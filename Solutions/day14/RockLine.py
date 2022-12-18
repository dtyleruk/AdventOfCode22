import re

from Solutions.day14.Coordinate import Coordinate, get_coordinates_between_two, get_top_corner_of_coord_list, \
    get_bottom_corner_of_coord_list


class RockLine:
    def __init__(self, input_string):
        super().__init__()
        x1 = re.split(" ->", input_string)

        self.rock_edges = []
        for coord_string in x1:
            self.rock_edges.append(Coordinate.make_coord_from_string(coord_string))

        self.rock_tiles = set()
        self.gen_rock_coords()
        self.top_corner = get_top_corner_of_coord_list(self.rock_tiles)
        self.bottom_corner = get_bottom_corner_of_coord_list(self.rock_tiles)

    def gen_rock_coords(self):
        rock_tile_list = []
        for i in range(1, len(self.rock_edges)):
            for coord in get_coordinates_between_two(self.rock_edges[i-1], self.rock_edges[i]):
                rock_tile_list.append(coord)
        self.rock_tiles = set(rock_tile_list)