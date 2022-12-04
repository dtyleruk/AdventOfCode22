from Solutions.day4.AssignmentPair import AssignmentPair

# Read input section
f = open("../../Inputs/day4/part1.dat", "r")
bag_contents = f.read().splitlines()


ass_pairs = []

for bag in bag_contents:
    ass_pairs.append(AssignmentPair(bag))


assignment_pairs_containing_each_other_count = 0

assignment_pairs_overlapping_count = 0

for pair in ass_pairs:
    if pair.does_one_assignment_range_fully_contain_other():
        assignment_pairs_containing_each_other_count += 1
    if pair.do_assignemnts_overlap():
        assignment_pairs_overlapping_count += 1


print("Count of ass pairs containing each other is: ", assignment_pairs_containing_each_other_count)
print("Count of ass pairs overlapping is: ", assignment_pairs_overlapping_count)
