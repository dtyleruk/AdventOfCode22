from Solutions.day9.Rope import Instruction, Rope

# Read input section
f = open("../../Inputs/day9/part1.dat", "r")
input = f.read().splitlines()

rope = Rope(input, 2)

rope.run_all_moves()

print("The tail has been in: ", rope.squares_tail_has_been_in(), " squares")

rope2 = Rope(input, 10)

rope2.run_all_moves()
print("The tail has been in: ", rope2.squares_tail_has_been_in(), " squares")