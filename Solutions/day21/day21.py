import math
from fractions import Fraction

from Solutions.day21.YellingMonkey import YellingMonkey

f = open("../../Inputs/day21/part1.dat", "r")
input = f.read().splitlines()


def make_monkey_dict(input):
    monkey_dict = dict()
    for input_line in input:
        monkey = YellingMonkey(input_line, monkey_dict)
        monkey_dict[monkey.name] = monkey
    return monkey_dict


# Part 1
monkey_dict = make_monkey_dict(input)
monkey_dict["root"].calc_value()
print("Root's number is: ", monkey_dict["root"].value)

# Part 2
# Edit inputs
monkey_dict = make_monkey_dict(input)
monkey_dict["root"].operation = "="
monkey_dict["humn"].value = ["x"]

monkey_dict["root"].calc_value()


def perform_reverse_operation(RHS, operation):

    # intermediate value for debugging
    LHS = RHS
    if operation[0] == "+":
        LHS -= operation[1]
    elif operation[0] == "-":
        LHS += operation[1]
    elif operation[0] == "*":
        LHS /= operation[1]
        # LHS //= operation[1]
    elif operation[0] == "/":
        LHS *= operation[1]
    else:
        raise Exception

    # if operation[0] == "+":
    #     if LHS + operation[1] != RHS:
    #         raise
    # if operation[0] == "-":
    #     if LHS - operation[1] != RHS:
    #         raise
    # if operation[0] == "*":
    #     if LHS * operation[1] != RHS:
    #         raise
    # if operation[0] == "/":
    #     if LHS // operation[1] != RHS:
    #         raise

    return LHS


def unpick_operation(operation_list):
    RHS = operation_list.pop(-1)[1]
    while len(operation_list) > 1:
        print("RHS:", RHS, " Operation:", operation_list[-1])
        RHS = perform_reverse_operation(RHS, operation_list.pop(-1))


    return RHS



value_to_yell = unpick_operation(monkey_dict["root"].value)
print("Value for human to yell is:", value_to_yell)