from Solutions.day14 import RockLine
from Solutions.day14.Coordinate import get_top_corner_of_coord_list, get_bottom_corner_of_coord_list
import numpy as np


class RockMap:
    def __init__(self, rock_lines, is_infinite_grid):
        super().__init__()
        self.top_corner = None
        self.bottom_corner = None
        self.gen_bottom_and_top_coners(rock_lines)
        self.grid = np.zeros((self.top_corner.x+1100, self.top_corner.y+40))

        if not is_infinite_grid:
            self.grid[:,(self.top_corner.y+2)] = 1

        self.sand_dropped = 0

        self.sand_drop = 500
        self.last_move = "FIRST"

        for rock_line in rock_lines:
            for coord in rock_line.rock_tiles:
                self.grid[coord.x, coord.y] = 1

    def gen_bottom_and_top_coners(self, rock_lines):
        top_corners = []
        bottom_corners = []
        for rock_line in rock_lines:
            top_corners.append(rock_line.top_corner)
            bottom_corners.append(rock_line.bottom_corner)
        self.top_corner = get_top_corner_of_coord_list(top_corners)
        self.bottom_corner = get_bottom_corner_of_coord_list(bottom_corners)

    def drop_n_sand(self, n):
        for i in range(0, n):
            self.drop_sand()

    def how_many_sand_can_be_dropped(self):
        while self.last_move != "FALL" and self.last_move != "STUCK_AT_TOP":
            self.drop_sand()

    def drop_sand(self):
        self.sand_dropped += 1
        sand_location = (500, 0)
        if self.grid[sand_location] == 2:
            self.last_move = "STUCK_AT_TOP"
            return

        self.grid[sand_location] = 2

        sand_moved = True
        while sand_moved:
            new_sand_location = self.attempt_move(sand_location)
            if sand_location == new_sand_location:
                sand_moved = False
            else:
                sand_location = new_sand_location

    def attempt_move(self, sand_location):
        # Check down
        try:
            if self.grid[sand_location[0], sand_location[1]+1] == 0:
                new_sand_location = (sand_location[0], sand_location[1]+1)
                self.last_move = "DOWN"
            # Check right
            elif self.grid[sand_location[0] - 1, sand_location[1] + 1] == 0:
                new_sand_location = (sand_location[0] - 1, sand_location[1] + 1)
                self.last_move = "RIGHT"
            # Check left
            elif self.grid[sand_location[0]+1, sand_location[1]+1] == 0:
                new_sand_location = (sand_location[0]+1, sand_location[1]+1)
                self.last_move = "LEFT"

            else:
                new_sand_location = sand_location
                self.last_move = "NO_MOVE"
            self.grid[sand_location] = 0
            self.grid[new_sand_location] = 2
            return new_sand_location

        except:
            self.last_move = "FALL"
