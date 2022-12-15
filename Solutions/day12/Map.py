import numpy as np
import string


class Map:
    def __init__(self, input_string):
        super().__init__()
        self.height_map = generate_height_map(input_string)
        self.start = find_letter(input_string, "S")
        self.end = find_letter(input_string, "E")

        self.visited = set([self.start])
        self.current_locations = set([self.start])
        self.step_count = 0

    def reset(self):
        self.visited = set([self.start])
        self.current_locations = set([self.start])
        self.step_count = 0

    def set_start(self, start):
        self.start = start
        self.reset()

    def find_shortest_path_to_end(self):
        while not self.has_found_end() and not self.is_stuck():
            self.take_step()
        if self.is_stuck():
            print("This run got stuck after", self.step_count, "steps, setting a stupid high step count")
            self.step_count = 1e100

    def take_step(self):
        new_locations = set([])
        for location in self.current_locations:
            this_location_possible_moves = self.calc_possible_moves(location)
            for move_location in this_location_possible_moves:
                new_locations.add(move_location)
        # Remove any that are found in self.visited to avoid loop paths
        new_locations = new_locations.difference(self.visited)
        # Add them to self.visited so they aren't looped back to
        for new_location in new_locations:
            self.visited.add(new_location)
        # Make it self.current_locations to know where to step from next
        self.current_locations = new_locations
        self.step_count += 1

    def has_found_end(self):
        if self.visited.__contains__(self.end):
            return True
        return False

    def is_stuck(self):
        if len(self.current_locations) == 0:
            return True
        return False

    def calc_possible_moves(self, location):
        possible_moves = []
        this_location_height = self.height_map[location]
        # Need to look up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            if self.can_move_in_direction(location, direction):
                possible_moves.append(add_two_coords(location, direction))
        return possible_moves

    def can_move_in_direction(self, location, direction):
        move_check_location = add_two_coords(location, direction)
        if not self.is_location_valid(move_check_location):
            return False
        return can_move_from_a_to_b(self.height_map[location], self.height_map[move_check_location])

    def is_location_valid(self, location):
        if min(location) < 0:
            return False
        if location[0] >= self.height_map.shape[0]:
            return False
        if location[1] >= self.height_map.shape[1]:
            return False
        return True


def can_move_from_a_to_b(a,b):
    if b <= a+1:
        return True
    return False


def add_two_coords(a, b):
    return (a[0] + b[0], a[1] + b[1])


def find_letter(input_string, letter_to_find):
    for row in range(0, len(input_string)):
        letter_index = input_string[row].find(letter_to_find)
        if letter_index != -1:
            return (row, letter_index)


def generate_height_map(input_string):
    height_map = []
    for line in input_string:
        this_height_line = []
        for char in line:
            if char == "S":
                this_height_line.append(string.ascii_lowercase.find('a'))
            elif char == "E":
                this_height_line.append(string.ascii_lowercase.find('z'))
            else:
                this_height_line.append(string.ascii_lowercase.find(char))

        height_map.append(this_height_line)

    return np.array(height_map)
