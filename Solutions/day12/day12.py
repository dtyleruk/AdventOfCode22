from Solutions.day12.Map import Map
import re

# Read input section
f = open("../../Inputs/day12/part1.dat", "r")
input = f.read().splitlines()
height_map = Map(input)

# Each coord needs a set of valid directions?
height_map.find_shortest_path_to_end()

print("Shortest path to end takes:", height_map.step_count, "steps")

# Brute force part 2 because I'm lazy:
a_count = 0
for row in range(0, height_map.height_map.shape[0]):
    for col in range(0, height_map.height_map.shape[1]):
        if height_map.height_map[(row, col)] == 0:
           a_count += 1

# Eesh, 2000 ish is a fair few
search_count = 0
min_steps = 1e6
for row in range(0, height_map.height_map.shape[0]):
    for col in range(0, height_map.height_map.shape[1]):
        if height_map.height_map[(row, col)] == 0:
            search_count += 1
            print("Doing search:", search_count, "of", a_count)
            height_map.reset()
            height_map.set_start((row, col))
            height_map.find_shortest_path_to_end()
            if height_map.step_count < min_steps:
                min_steps = height_map.step_count
                print("New min steps found:", min_steps)

print("Min steps from any lowest starting point is:", min_steps)
