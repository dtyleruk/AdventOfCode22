# Read input section
f = open("../Inputs/day1/part1.dat", "r")
Lines = f.readlines()

elfs_items = []
this_elf = []

for line in Lines:
    this_line = line.split()
    if len(this_line) == 1:
        if len(this_line[0]) > 0:
            this_elf.append(int(this_line[0]))
    else:
        elfs_items.append(this_elf)
        this_elf = []

# Part 1, which elf has the most calories?
# Sum each elf's calorie count
elf_totals = []

for elf in elfs_items:
    elf_totals.append(sum(elf))

# Find which elf's sum is greatest
max_elf_food = max(elf_totals)

print("Max calorie elf value: ", max_elf_food)

# Part 2, Sum of the top 3 values in elf_totals
elf_totals.sort(reverse=True)

print("Total calorie count of top 3 elves: ", sum(elf_totals[:3]))
