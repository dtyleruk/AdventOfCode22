import re
import numpy as np



class Blizzard:
    def __init__(self, input):
        super().__init__()
        self.blizzard = read_initial_blizzard_state(input)
        self.blizzard_next_min = advance_blizzard(self.blizzard)
        self.age = 0
        entrance = np.where(self.blizzard == -2)
        self.locations = [(entrance[0][0], entrance[1][0])]
        self.max_location_row = 0
        self.min_location_row = self.blizzard.shape[1]

    def reset_min_max_rows(self):
        self.max_location_row = 0
        self.min_location_row = self.blizzard.shape[1]

    def step_down_until_done(self):

        self.locations = [(0,1)]
        self.reset_min_max_rows()

        while self.max_location_row < (self.blizzard.shape[0]-1):
            self.step_forward()
            self.update_max_location_row()

        return self.age

    def step_up_until_done(self):

        self.locations = [(self.blizzard.shape[0]-1, self.blizzard.shape[1]-2)]
        self.reset_min_max_rows()

        while self.min_location_row > 0:
            self.step_forward()
            self.update_min_location_row()

        return self.age

    def update_min_location_row(self):
        for location in self.locations:
            if location[0] < self.min_location_row:
                self.min_location_row = location[0]
                print("New min location row:",  self.min_location_row, "at age:", self.age)

    def update_max_location_row(self):
        for location in self.locations:
            if location[0] > self.max_location_row:
                self.max_location_row = location[0]
                print("New max location row:",  self.max_location_row, "at age:", self.age)

    def step_forward(self):
        self.age += 1
        self.locations = self.mark_all_possible_locations()
        self.blizzard = self.blizzard_next_min
        self.blizzard_next_min = advance_blizzard(self.blizzard)

    def mark_all_possible_locations(self):

        # For each location, check possible next locations.
        # You can move up, down, left, right or wait, only if there are no blizzards there
        next_locations = []
        for location in self.locations:
            if self.blizzard_next_min[location] == 0:
                next_locations.append(location)
            if location[0] != self.blizzard.shape[0]-1:
                if self.blizzard_next_min[location[0]+1, location[1]] == 0:
                    next_locations.append((location[0]+1, location[1]))
            if self.blizzard_next_min[location[0]-1, location[1]] == 0:
                next_locations.append((location[0]-1, location[1]))
            if self.blizzard_next_min[location[0], location[1]+1] == 0:
                next_locations.append((location[0], location[1]+1))
            if self.blizzard_next_min[location[0], location[1]-1] == 0:
                next_locations.append((location[0], location[1]-1))

        return list(set(next_locations))


# Takes input with . # and >< and converts it to a numpy array
# Wall -5
# Empty space = 0
# Entrance -2, Exit -1? Not yet
# Blizzard up 1, down 2, right 4, left 8, something like that
def read_initial_blizzard_state(input):
    blizzard = []
    for row in input:
        row_input = []
        for char in row:
            if char == "#":
                row_input.append(-5)
            elif char == ".":
                row_input.append(0)
            elif char == "^":
                row_input.append(1)
            elif char == "v":
                row_input.append(2)
            elif char == ">":
                row_input.append(4)
            elif char == "<":
                row_input.append(8)
            else:
                exit("Unexpected input char:" + char)
        blizzard.append(row_input)

    blizzard_array = np.array(blizzard)

    entrance_ind = np.where(blizzard_array[0] == 0)
    blizzard_array[0][entrance_ind] = -2

    return blizzard_array

# Take an input blizzard and move all the blizzards
def advance_blizzard(blizzard):
    advanced_blizzard = np.where(blizzard > -4, 0, blizzard)

    for row in range(blizzard.shape[0]):
        for col in range(blizzard.shape[1]):
            if blizzard[row][col] <= 0:
                continue
            if blizzard[row][col] & 1 == 1: #Blizzard going up
                if blizzard[row-1][col] == -5:
                    advanced_blizzard[advanced_blizzard.shape[0] - 2][col] += 1
                else:
                    advanced_blizzard[row-1][col] += 1
            if blizzard[row][col] & 2 == 2: #Blizzard going down
                if blizzard[row + 1][col] == -5:
                    advanced_blizzard[1][col] += 2
                else:
                    advanced_blizzard[row + 1][col] += 2
            if blizzard[row][col] & 4 == 4: #Blizzard going right
                if blizzard[row][col+1] == -5:
                    advanced_blizzard[row][1] += 4
                else:
                    advanced_blizzard[row][col+1] += 4
            if blizzard[row][col] & 8 == 8: #Blizzard going left
                if blizzard[row][col - 1] == -5:
                    advanced_blizzard[row][advanced_blizzard.shape[1]-2] += 8
                else:
                    advanced_blizzard[row][col - 1] += 8


    return advanced_blizzard
