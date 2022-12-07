f = open("../Inputs/day6/part1.dat", "r")
input = f.read().splitlines()[0]

unChar = 14

for i in range(0, len(input)):
    if len(set(input[i:i+unChar])) == unChar:
        print("Part 2 answer is: ", i+unChar)
        stop()
