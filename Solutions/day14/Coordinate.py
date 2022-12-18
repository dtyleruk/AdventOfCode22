import re


class Coordinate:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # From string containing 'x,y'
    @staticmethod
    def make_coord_from_string(coord_string):
        each_part_string = re.split(",", coord_string)
        return Coordinate(int(each_part_string[0]), int(each_part_string[1]))

    def manhattan_distance_to_coord(self, coord):
        return abs(coord.x - self.x) + abs(coord.y - self.y)


def get_bottom_corner_of_coord_list(coord_list):
    if len(coord_list) == 0:
        return

    minx = 1e45
    miny = 1e45

    for coord in coord_list:
        if coord.x < minx:
            minx = coord.x
        if coord.y < miny:
            miny = coord.y

    return Coordinate(minx, miny)


def get_top_corner_of_coord_list(coord_list):
    if len(coord_list) == 0:
        return

    maxx = -1e45
    maxy = -1e45

    for coord in coord_list:
        if coord.x > maxx:
            maxx = coord.x
        if coord.y > maxy:
            maxy = coord.y

    return Coordinate(maxx, maxy)


def get_coordinates_between_two(c1, c2):
    coord_list = []
    if c1.x == c2.x:
        for y in range(min(c1.y, c2.y), max(c1.y, c2.y)+1):
            coord_list.append(Coordinate(c1.x, y))
    elif c1.y == c2.y:
        for x in range(min(c1.x, c2.x), max(c1.x, c2.x)+1):
            coord_list.append(Coordinate(x, c1.y))
    else:
        exit("get_coordinates_between_two currently only works if x or y are the same")
    return coord_list