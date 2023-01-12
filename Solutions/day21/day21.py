from Solutions.day21.YellingMonkey import YellingMonkey

f = open("../../Inputs/day21/part1.dat", "r")
input = f.read().splitlines()

monkey_dict = dict()

for input_line in input:
    monkey = YellingMonkey(input_line, monkey_dict)
    monkey_dict[monkey.name] = monkey

monkey_dict["root"].calc_value()
print("Root's number is: ", monkey_dict["root"].value)


