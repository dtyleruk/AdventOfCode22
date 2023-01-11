from Inputs.day20.test_input import *


# Make each value a tuple. It's value plus has it been moved
tuples = []
for i in input:
    tuples.append((i,False))


def do_normal_move(tuples, index_to_move, new_position):
    to_insert = tuples.pop(index_to_move)
    tuples.insert(new_position, (to_insert[0], True))
    return tuples


def move_element(tuples, index_to_move):
    belb = 1
    distance_to_move = tuples[index_to_move][0]
    new_position = (distance_to_move + index_to_move)

    if len(tuples) > new_position >= 0:
        tuples = do_normal_move(tuples, index_to_move, new_position)

    elif new_position > len(tuples):
        # Rearrange to put element to move at the front of the vector
        tuples = tuples[index_to_move:len(tuples)] + tuples[0:index_to_move]
        # Do move
        tuples = do_normal_move(tuples, 0, distance_to_move)
        # Rearrange back
        tuples = tuples[(len(tuples)-index_to_move):len(tuples)] + tuples[0:(len(tuples)-index_to_move)]

    elif new_position > len(tuples) * 2:
        raise Exception

    else: # new_position < 0
        tuples = tuples[(index_to_move+1):len(tuples)] + tuples[0:(index_to_move+1)]
        tuples = do_normal_move(tuples, len(tuples)-1, distance_to_move)
        tuples = tuples[(len(tuples) - (index_to_move)):len(tuples)] + tuples[0:(len(tuples) - (index_to_move))]

    # Probably don't need to return this
    return tuples


curr_index = 0
values_moved = 0

while values_moved < len(tuples):
    print(curr_index, " ", values_moved, " ", tuples)
    if not tuples[curr_index][1]:
        tuples = move_element(tuples, curr_index)
        if tuples[curr_index][0] < 0:
            curr_index += 1
        values_moved += 1

    else:
        curr_index += 1
    if curr_index == len(tuples):
        curr_index = 0

print(tuples)