from Solutions.day11.Monkey import MonkeyGroup

# Read input section
f = open("../../Inputs/day11/part1.dat", "r")
input = f.read().splitlines()

monkeys = MonkeyGroup(input, 3.0)
monkeys.perform_n_rounds(20)
print("Monkey business after 20 rounds: ", monkeys.calc_monkey_business())


# Part 2, no worry divider
monkeys = MonkeyGroup(input, 1.0)
monkeys.perform_n_rounds(10000)
print("Monkey business after 10000 rounds: ", monkeys.calc_monkey_business())