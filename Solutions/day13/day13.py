# from Inputs.day13.test_data import *
from Inputs.day13.part1 import *

results = []
for input_pair in input_pairs:
    results.append(input_pair.are_lists_in_correct_order())

# Now sum index of matching values
index_sum = 0
for index in range(0, len(results)):
    if results[index]:
        index_sum += (1+index)

print("Sum of indicies of ordered pairs:", index_sum)

# For part 2, extract pairs back into single packets
packet_list = [ [[2]], [[6]] ]

for input_pair in input_pairs:
    packet_list.append(input_pair.list1)
    packet_list.append(input_pair.list2)

def swap_els(list, index):
    list[index], list[index+1] = list[index+1], list[index]
    return list

# To keep structure of part 1, I'm going to do make a pair, see if it's sorted, and bubble sort through many times

changes = 1

while changes > 0:
    changes = 0
    for index in range(0, len(packet_list)-1):
        pair_to_compare = InputPair(packet_list[index], packet_list[index+1])
        result = pair_to_compare.are_lists_in_correct_order()
        if not result:
            packet_list = swap_els(packet_list, index)
            changes += 1
    # print("Changes from this iteration of bubble sort:", changes)

print("Location of divider packets are:", packet_list.index([[2]]), packet_list.index([[6]]))
print("Decoder key is:", (packet_list.index([[2]]) + 1) * (packet_list.index([[6]])+1))


belb = 1
