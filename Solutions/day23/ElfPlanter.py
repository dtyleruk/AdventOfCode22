import re
import numpy as np
from Solutions.day14.Coordinate import Coordinate


class ElfPlanter:
    def __init__(self, input, pad_size=10):
        super().__init__()
        self.initial_elf_locations_matrix = read_initial_elf_locations_as_matrix(input, pad_size)
        self.elf_locations = self.initial_elf_locations_matrix.copy()
        # self.elfs = np.argwhere(self.initial_elf_locations_matrix == 1)
        self.check_order = [("N", [(-1, -1), (-1, 0), (-1, 1)]),
                            ("S", [(1, -1), (1, 0), (1, 1)]),
                            ("W", [(-1, -1), (0, -1), (1, -1)]),
                            ("E", [(-1, 1), (0, 1), (1, 1)])
                            ]

    def cycle_check_order(self):
        self.check_order.append(self.check_order[0])
        self.check_order.pop(0)

    def plan_n_moves(self, n):
        for move in range(0, n):
            self.plan_moves()

    def plan_all_moves(self):
        did_any_elves_move = True
        round_count = 0
        elf_locations = self.elf_locations
        new_locations = self.elf_locations
        while did_any_elves_move:
            elf_locations = self.elf_locations
            round_count += 1
            new_locations = self.plan_moves()
            if (elf_locations == new_locations).all():
                did_any_elves_move = False
            print(round_count)
        return round_count

    def plan_moves(self):
        new_locations = self.elf_locations.copy()
        new_locations.fill(0)
        elfs = np.argwhere(self.elf_locations == 1)
        elfs_current_locations_as_tuples = []
        elfs_proposed_locations = []
        for elf in elfs:
            elfs_current_locations_as_tuples.append(tuple(elf))
            new_spot = self.plan_single_move(tuple(elf))
            elfs_proposed_locations.append(new_spot)
            new_locations[new_spot] += 1

        # Now execute moves if appropriate
        final_locations = self.elf_locations.copy()
        final_locations.fill(0)
        for elf_index in range(0, len(elfs_proposed_locations)):
            proposed_location = elfs_proposed_locations[elf_index]
            if new_locations[proposed_location] == 1:
                final_locations[proposed_location] = 1
            elif new_locations[proposed_location] > 1:
                final_locations[elfs_current_locations_as_tuples[elf_index]] = 1
            else:
                exit("I don't know how, but new location is 0 or less.")

        self.elf_locations = final_locations

        self.cycle_check_order()

        return final_locations

    # Check where a single elf wants to go in the planning phase
    def plan_single_move(self, co_ord):

        if not self.does_elf_need_to_move(co_ord):
            return co_ord

        for check_direction in self.check_order:
            can_move_in_this_direction = True
            for single_check_direction in check_direction[1]:
                if self.elf_locations[add_tuples(co_ord, single_check_direction)] == 1:
                    can_move_in_this_direction = False
                    break
            if can_move_in_this_direction:
                return add_tuples(co_ord, check_direction[1][1])
        #If all directions fail, don't move and return orig co_ordinate
        return co_ord

    # Check all surrounding squares of elf. If they are all empty, the elf doesn't need to move
    def does_elf_need_to_move(self, co_ord):
        for check_direction in self.check_order:
            for single_check_direction in check_direction[1]:
                if self.elf_locations[add_tuples(co_ord, single_check_direction)] == 1:
                    return True
        return False

    def find_area_of_smallest_encompossing_rectangle(self):
        elfs = np.argwhere(self.elf_locations == 1)
        min_vals = np.amin(elfs, axis=0)
        max_vals =  np.amax(elfs, axis=0)

        height = max_vals[0] - min_vals[0] + 1
        width = max_vals[1] - min_vals[1] + 1

        return (height * width) - elfs.shape[0]



def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

# Takes input with . and # and converts it to a numpy array
def read_initial_elf_locations_as_matrix(input, pad_size):
    elf_list = []
    for row in input:
        row_input = []
        for char in row:
            if char == "#":
                row_input.append(1)
            else:
                row_input.append(0)
        elf_list.append(row_input)

    elf_array = np.array(elf_list)

    elf_array = np.append(elf_array, np.zeros((pad_size, elf_array.shape[1])), axis=0)
    elf_array = np.append(np.zeros((pad_size, elf_array.shape[1])), elf_array, axis=0)

    elf_array = np.append(np.zeros((elf_array.shape[0], pad_size)), elf_array, axis=1)
    elf_array = np.append(elf_array, np.zeros((elf_array.shape[0], pad_size)), axis=1)

    return elf_array
