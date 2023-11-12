import numpy as np
import re

from Solutions.day22.CubeNavigator import CubeNavigator
from Solutions.day22.GridNavigator import GridNavigator

# f = open("../../Inputs/day22/part1.dat", "r")
f = open("../../Inputs/day22/test_input.dat", "r")
input = f.read().splitlines()
grid = GridNavigator(input)

grid.perform_all_instructions()

#Part 2
cube = CubeNavigator(input, 4)

cube.move_off_edge("Bottom", 1, 2, 2)

cube.do_orientations_match(1,2)

print("Final location is: ", grid.location)
print("Final direction is: ", grid.direction)
print("Final password is: ", grid.calc_final_password())
belb = 1


