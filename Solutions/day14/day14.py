from Solutions.day14.RockLine import RockLine

# Read input section
from Solutions.day14.RockMap import RockMap

f = open("../../Inputs/day14/part1.dat", "r")
input = f.read().splitlines()

rock_lines = []

for input_line in input:
    rock_lines.append(RockLine(input_line))

rock_map = RockMap(rock_lines, True)

rock_map.how_many_sand_can_be_dropped()

print("Sand dropped with infinite floor is: ", rock_map.sand_dropped - 1)

rock_map = RockMap(rock_lines, False)
rock_map.how_many_sand_can_be_dropped()
print("Sand dropped with floor is: ", rock_map.sand_dropped - 1)