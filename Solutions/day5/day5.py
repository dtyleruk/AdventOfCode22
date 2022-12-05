import re
import copy

# Read input section
f = open("../../Inputs/day5/part1.dat", "r")
stack_instructions = f.read().splitlines()


def find_stack_label_line(stack_instructions):
    for line_index in range(0, len(stack_instructions)):
        if stack_instructions[line_index][:3] == " 1 ":
            return line_index


def split_stack_line_into_buckets(stack_information):
    stack_info = []
    for char_index in range(0, int(len(stack_information)/4 + 1)):
        stack_info.append(stack_information[char_index*4+1])
    return stack_info


def extract_starting_stack_vectors(stack_instructions, stack_label_index):

    full_stack_info = []
    for stack_info_index in range(stack_label_index-1, -1, -1):
        full_stack_info.append(split_stack_line_into_buckets(stack_instructions[stack_info_index]))

    # Now turn stack info sideways to have a vector for each stack
    stack_vectors = []

    # Length of first stack will give number of stacks, as well as the char at the bottom of each stack
    stack_count = len(full_stack_info[0])
    for char in full_stack_info[0]:
        stack_vectors.append([char])

    for stack_info in full_stack_info[1:]:
        for stack_num in range(0, len(stack_info)):
            if stack_info[stack_num] != "" and stack_info[stack_num] != " ":
                stack_vectors[stack_num].append(stack_info[stack_num])

    return stack_vectors


# instruction in the form move x from n to m
def parse_move_instruction(instruction_string, stack_vectors, CrateMoverVersion):
    instruction_values = re.findall('\d+', instruction_string)

    move_count = int(instruction_values[0])
    move_from = int(instruction_values[1]) - 1
    move_to = int(instruction_values[2]) - 1

    stack_len = len(stack_vectors[move_from])

    to_move = stack_vectors[move_from][stack_len-move_count:stack_len]

    if CrateMoverVersion == 9000:
        to_move.reverse()

    stack_vectors[move_to].extend(to_move)
    del stack_vectors[move_from][stack_len-move_count:stack_len]

    return stack_vectors


# Find line with bucket numbers and iterate backwards from there.
stack_label_index = find_stack_label_line(stack_instructions)
stack_vectors = extract_starting_stack_vectors(stack_instructions, stack_label_index)

move_instructions = stack_instructions[stack_label_index+2:]

stack_vectors_9000 = copy.deepcopy(stack_vectors.copy())
stack_vectors_9001 = copy.deepcopy(stack_vectors.copy())

for move_instruction in move_instructions:
    stack_vectors_9000 = parse_move_instruction(move_instruction, stack_vectors_9000, 9000)

for move_instruction in move_instructions:
    stack_vectors_9001 = parse_move_instruction(move_instruction, stack_vectors_9001, 9001)


# Finally print the combination of what is at the top of each stack
stack_tops_9000 = ''
for stack in stack_vectors_9000:
    stack_tops_9000 = stack_tops_9000 + stack[len(stack) - 1][0]

stack_tops_9001 = ''
for stack in stack_vectors_9001:
    stack_tops_9001 = stack_tops_9001 + stack[len(stack) - 1][0]

print("Values at the top of each stack from CrateStacker9000 are:", stack_tops_9000)
print("Values at the top of each stack from CrateStacker9001 are:", stack_tops_9001)

