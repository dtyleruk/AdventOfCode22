import string
priority = string.ascii_lowercase + string.ascii_uppercase


def calc_total_priority_value(letters):
    total_priority_value = 0
    # Now sum them according to their priorities
    for letter in letters:
        total_priority_value += (priority.find(letter) + 1)
    return total_priority_value

# Read input section
f = open("../Inputs/day3/part1.dat", "r")
bag_contents = f.read().splitlines()

# Each bag has a tuple with the contents of each compartment
split_bags = []

for bag in bag_contents:
    items_per_compartment = int(len(bag)/2)
    this_contents = (set(bag[:items_per_compartment]), set(bag[items_per_compartment:]))
    split_bags.append(this_contents)

shared_letters = []

# Part 1, determine duplicate letter of each bag's pair of compartments.
for bag in split_bags:
    shared_letters.append(list(bag[0].intersection(bag[1]))[0])

print("Total priority value is: ", calc_total_priority_value(shared_letters))


# Part 2. Build groups of three
groups = []
for i in range(int(len(bag_contents)/3)):
    group_ind = 3*i
    this_group = [set(bag_contents[group_ind]), set(bag_contents[group_ind+1]), set(bag_contents[group_ind+2])]
    groups.append(this_group)

# Now for each group of three bags, find the letter in all of them
badges = []

for group in groups:
    badges.append(list(group[0].intersection(group[1]).intersection(group[2]))[0])

print("Total priority of badges is: ", calc_total_priority_value(badges))
