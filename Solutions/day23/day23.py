from Solutions.day23.ElfPlanter import ElfPlanter

# f = open("../../Inputs/day23/small_test_input.dat", "r")
# f = open("../../Inputs/day23/large_test_input.dat", "r")
f = open("../../Inputs/day23/part1.dat", "r")
input = f.read().splitlines()

planter = ElfPlanter(input, pad_size=110)

# Part 1
# planter.plan_n_moves(10)
# rectangle_area = planter.find_area_of_smallest_encompossing_rectangle()
# print("Area of rectangle after 10 rounds is:", rectangle_area)

# Part 2
round_count_to_completion = planter.plan_all_moves()
print("Rounds to completion: ", round_count_to_completion)




