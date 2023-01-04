import numpy as np

from Solutions.day17.TetrisBoard import TetrisBoard


def get_wind_array_from_input(input_string):
    wind_array = []
    for char in input_string:
        if char == "<":
            wind_array.append(-1)
        else:
            wind_array.append(1)
    return wind_array


f = open("../../Inputs/day17/part1.dat", "r")
wind_array = get_wind_array_from_input(f.read().splitlines()[0])
board = TetrisBoard(wind_array)
board.make_n_pieces(2022)

# board.print_board(3070)
print("Highest point on the tower after 2022 steps is:", board.highest_point_on_tower())
belb = 1

