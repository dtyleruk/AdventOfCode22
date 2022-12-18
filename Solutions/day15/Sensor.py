from Solutions.day14.Coordinate import *

import re

class Sensor:
    def __init__(self, input_string):
        super().__init__()
        self.location = None
        self.nearest_beacon = None
        self.parse_coords(input_string)
        self.distance_to_beacon = self.calc_distance_to_beacon()

    def parse_coords(self, input_string):
        coords = re.findall("[-0-9]+", input_string)
        if len(coords) != 4:
            raise Exception("There are not 4 coord numbers in input")

        self.location = Coordinate(int(coords[0]), int(coords[1]))
        self.nearest_beacon = Coordinate(int(coords[2]), int(coords[3]))

    # Returns range in which there is not a beacon
    def which_y_elements_of_row_x_cannot_contain_beacon(self, row):
        row_offset = abs(row - self.location.y)
        if row_offset > self.distance_to_beacon:
            return None

        # How much of the row in question is blocked in either direction
        pm_row_distance = self.distance_to_beacon - row_offset
        return (self.location.x - pm_row_distance, self.location.x + pm_row_distance)

    def calc_distance_to_beacon(self):
        return self.location.manhattan_distance_to_coord(self.nearest_beacon)
