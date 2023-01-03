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


f = open("../../Inputs/day17/test_data.dat", "r")
wind_array = get_wind_array_from_input(f.read().splitlines()[0])
board = TetrisBoard(wind_array)
board.make_n_pieces(3)

belb = 1

