import numpy as np
import re

class GridNavigator:
    def __init__(self, input):
        self.grid = convert_grid_to_array(input[:-2])
        self.instructions = convert_instructions_to_list(input[-1])

        self.location = find_start_location(self.grid)
        self.direction = 0 # Index in self.directions
        self.instruction_index = 0

        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # R,D,L,U

        self.edges = self.calc_edges() # First non zero element in each direction, corresponding to direction of travel.
         # Eg, first el of directions is Right, so first el of edges is the left hand side

    # From each direction, find the first non-zero element
    def calc_edges(self):
        left_edges = []
        right_edges = []
        top_edges = [] # Top means highest value of array
        bottom_edges = []

        for i in range(0, self.grid.shape[0]):
            non_zero_elements = np.where(self.grid[i] != 0)
            left_edges.append(non_zero_elements[0][0])
            right_edges.append(non_zero_elements[0][-1])

        for i in range(0, self.grid.shape[1]):
            non_zero_elements = np.where(self.grid[:,i] != 0)
            bottom_edges.append(non_zero_elements[0][-1])
            top_edges.append(non_zero_elements[0][0])

        return (left_edges, top_edges, right_edges, bottom_edges)

    def perform_all_instructions(self):
        for instruction_index in range(0, len(self.instructions)):
            self.perform_instruction(instruction_index)

    def perform_instruction(self, instruction_index):

        instruction = self.instructions[instruction_index]

        # print("Location: ", self.location, " direction:", self.direction, " instruction: ", instruction)

        if type(instruction) == int:
            self.perform_numeric_instruction(instruction)
        else:
            self.perform_rotation_instruction(instruction)

    # Walk in direction for given length
    # Until I figure out if it's too slow, just do it one step at a time for now
    def perform_numeric_instruction(self, instruction):
        distance_left = instruction
        direction = self.directions[self.direction]
        while distance_left > 0:
            distance_left -= 1
            self.take_step(direction)

    def take_step(self, direction):
        target_location = ((self.location[0] + direction[0]) % self.grid.shape[0], (self.location[1] + direction[1]) % self.grid.shape[1])

        # This needs to wrap around
        if self.grid[target_location] == 0:
            target_location = self.wrap(target_location)

        if self.grid[target_location] == 1:
            self.location = target_location

    # Determine where to go if the next square is in the void
    def wrap(self, target_location):
        if self.direction == 0: # Going Right
            return (target_location[0], self.edges[self.direction][self.location[0]])
        elif self.direction == 1: # Going Down
            return (self.edges[self.direction][self.location[1]], target_location[1])
        elif self.direction == 2: # Going Left
            return (target_location[0], self.edges[self.direction][self.location[0]])
        elif self.direction == 3: # Going Up
            return (self.edges[self.direction][self.location[1]], target_location[1])
        else:
            raise Exception

    # Change direction, R for clockwise, L for anti-clockwise
    def perform_rotation_instruction(self, instruction):
        if instruction == "R":
            self.direction = (self.direction + 1) % 4
        elif instruction == "L":
            self.direction = (self.direction - 1) % 4
        else:
            raise Exception

    def calc_final_password(self):
        return 1000 * (self.location[0]+1) + 4 * (self.location[1]+1) + self.direction

def get_grid_width(grid):
    max_width = 0
    for line in grid:
        if len(line) > max_width:
            max_width = len(line)
    return max_width


def convert_grid_to_array(grid):
    grid_width = get_grid_width(grid)

    for i in range(len(grid)):
        grid[i] = list(grid[i].replace("#", "2").replace(".", "1").replace(" ", "0"))
        grid[i] = [int(x) for x in grid[i]]
        if len(grid[i]) < grid_width:
            grid[i] += [0] * (grid_width - len(grid[i]))

    return np.array(grid, dtype=np.int)


def convert_instructions_to_list(instructions):
    return [int(i) if i.isdigit() else i for i in re.findall(r'\d+|\D+', instructions)]


# First open space on the top row
def find_start_location(grid):
    return (0, np.where(grid[1,] == 1)[0][0])

