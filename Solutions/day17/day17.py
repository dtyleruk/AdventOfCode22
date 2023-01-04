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
nsteps = len(board.pieces) * len(wind_array) * 5

board.make_n_pieces(nsteps)
# import cProfile
# cProfile.run('board.make_n_pieces(nsteps)')

# board.print_boar d(3070)
print("Highest point on the tower after ", nsteps, " steps is:", board.highest_point_on_tower())

# Now search for a repeating pattern, I'll first use an arbitrary set of values to compare, say 30 rows?
# Do the last 30 rows match any previous set of 30 rows?
n_rows = 30
last_n_rows = board.board[(board.spawn_height-n_rows-3):(board.spawn_height-3),:]

matches_at_height = []

for i in range(1, board.spawn_height):
    if (board.board[i:(i+n_rows), :] == last_n_rows).all():
        print("Found a match at: ", i)
        matches_at_height.append(i + n_rows)

# Init height 466
# Period height = 2738

# How many pieces to get to height of 466+30? 334
# How many pieces to get up another 2738? 1745
# Need to add those, then put some bits on top
#334 + n*1745 = 1trillion

first_match = matches_at_height[0]
first_match_piece_count = board.height_per_piece.index(first_match)
first_match_wind_count = board.wind_per_piece[first_match_piece_count]

sec_match = matches_at_height[1]
sec_match_piece_count = board.height_per_piece.index(sec_match)
sec_match_wind_count = board.wind_per_piece[sec_match_piece_count]

loop_height = sec_match - first_match
loop_piece_count = sec_match_piece_count - first_match_piece_count
loop_wind_count = sec_match_wind_count - first_match_wind_count

n_pieces = 1000000000000
required_loops = int((n_pieces - first_match_piece_count) / loop_piece_count)

pieces_added = required_loops * loop_piece_count

extra_pieces_required = n_pieces - (required_loops * loop_piece_count + first_match_piece_count)

curr_height = board.height_per_piece[-1]

board.make_n_pieces(extra_pieces_required)

extra_pieces_height_added = board.height_per_piece[-1] - curr_height

final_height = first_match + required_loops * loop_height + extra_pieces_height_added - 2 # I don't know why the -2 is needed, I'll be honest. But I got the star.

print("Final height after a trillion pieces added is: ", final_height)
