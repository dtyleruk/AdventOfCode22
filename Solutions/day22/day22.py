import numpy as np
import re

from Solutions.day22.GridNavigator import GridNavigator

f = open("../../Inputs/day22/part1.dat", "r")
input = f.read().splitlines()
grid = GridNavigator(input)

grid.perform_all_instructions()

print("Final location is: ", grid.location)
print("Final direction is: ", grid.direction)
print("Final password is: ", grid.calc_final_password())
belb = 1


