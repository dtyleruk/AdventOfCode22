from Inputs.day20.part1 import *

# input = [0,0,0,0,8]
# input = [0,0,0,-3,-8]
# input = [0, 0, 0, 0, -51]

# Make each value a tuple. It's value plus has it been moved


def make_tuples(input):
    tuples = []
    for i in range(0, len(input)):
        tuples.append((input[i], i))
    return tuples

def do_normal_move(tuples, index_to_move, new_position):
    to_insert = tuples.pop(index_to_move)
    tuples.insert(new_position, to_insert)
    return tuples


def move_element(tuples, index_to_move):
    distance_to_move = tuples[index_to_move][0]
    new_position = (distance_to_move + index_to_move)

    if len(tuples) > new_position >= 0:
        tuples = do_normal_move(tuples, index_to_move, new_position)

    elif new_position > len(tuples):

        # Rearrange to put element to move at the front of the vector
        tuples = tuples[index_to_move:len(tuples)] + tuples[0:index_to_move]

        # Shift elements along if there is a loopy loop
        if int(distance_to_move/len(tuples)) > 0:
            loops_remainder = 1
            if int(distance_to_move / len(tuples)) > 1:
                loops = int(distance_to_move / len(tuples))
                # Every n-1 loops of n gives the same result
                loops_remainder = loops % (len(tuples)-1)

            # Need to shift all the other elements
            tuples = tuples[0:1] + tuples[(loops_remainder+1):len(tuples)] + tuples[1:(loops_remainder+1)]

        # Do move
        tuples = do_normal_move(tuples, 0, distance_to_move%len(tuples))

    else: # new_position < 0
        tuples = tuples[(index_to_move+1):len(tuples)] + tuples[0:(index_to_move+1)]

        # Shift elements along if there is a loopy loop
        if int(abs(distance_to_move) / len(tuples)) > 0:
            loops_remainder = 1
            if int(abs(distance_to_move) / len(tuples)) > 1:
                loops = int(-distance_to_move / len(tuples))
                # Every n-1 loops of n gives the same result
                loops_remainder = loops % (len(tuples) - 1)
            # Need to shift all the other elements
            tuples = tuples[-(loops_remainder+1):-1] + tuples[:-(loops_remainder+1)] + tuples[-1:]

        tuples = do_normal_move(tuples, len(tuples)-1,  -(-distance_to_move%len(tuples)))

    # Probably don't need to return this
    return tuples


def mix_values(tuples):

    curr_index = 0
    values_moved = 0

    while values_moved < len(tuples):
        # print(curr_index, " ", values_moved, " ", tuples)
        # print(curr_index, " ", values_moved)
        if tuples[curr_index][1] == values_moved:
            tuples = move_element(tuples, curr_index)
            if tuples[curr_index][0] < 0:
                curr_index += 1
            values_moved += 1
            # print(curr_index, " ", values_moved, " ", tuples)
            # print(curr_index, " ", values_moved)

        else:
            curr_index += 1
        if curr_index == len(tuples):
            curr_index = 0

    return tuples


def perform_n_mixes(tuples, n):
    for i in range(0,n):
        print("Doing mix:", i+1, "of", n)
        tuples = mix_values(tuples)
    return tuples


def calc_grove_number(tuples):
    zero_index = 0
    for i in range(0, len(tuples)):
        if tuples[i][0] == 0:
            zero_index = i
            break
    return tuples[(1000+zero_index)%len(tuples)][0] + tuples[(2000+zero_index)%len(tuples)][0] + tuples[(3000+zero_index)%len(tuples)][0]


# Part 1
tuples = make_tuples(input)
tuples = mix_values(tuples)
grove_number = calc_grove_number(tuples)

print("Grove number is:", grove_number)

# Part 2
print("Starting part 2")
tuples = make_tuples(input)

decryption_key = 811589153
for i in range(0, len(tuples)):
    tuples[i] = (tuples[i][0] * decryption_key, tuples[i][1])

tuples = perform_n_mixes(tuples, 10)
grove_number = calc_grove_number(tuples)
print("Grove number is:", grove_number)
