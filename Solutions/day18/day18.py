import numpy as np

f = open("../../Inputs/day18/part1.dat", "r")
input = f.read().splitlines()

lava_coords = []

for line in input:
    split_string = line.split(',')
    lava_coords.append(tuple([(int(x)) for x in split_string]))


# Get max of each dimention
required_size = [0, 0, 0]
for lava_point in lava_coords:
    for dim in range(0,3):
        required_size[dim] = max(required_size[dim], lava_point[dim])

for dim in range(0,3):
    required_size[dim] += 2

lava_grid = np.zeros(tuple(required_size), dtype=int)

for lava_point in lava_coords:
    lava_grid[lava_point] = 1


# Now iterate over lava points to count sides that are exposed
def count_exposed_sides(location, lava_grid):
    # Need to check up and down in each location
    exposed_side_count = 0
    if lava_grid[location[0]+1, location[1], location[2]] == 0:
        exposed_side_count += 1
    if lava_grid[location[0]-1, location[1], location[2]] == 0:
        exposed_side_count += 1

    if lava_grid[location[0], location[1]-1, location[2]] == 0:
        exposed_side_count += 1
    if lava_grid[location[0], location[1]+1, location[2]] == 0:
        exposed_side_count += 1

    if lava_grid[location[0], location[1], location[2]-1] == 0:
        exposed_side_count += 1
    if lava_grid[location[0], location[1], location[2]+1] == 0:
        exposed_side_count += 1

    return exposed_side_count


total_exposed_sides = 0
for lava_point in lava_coords:
    total_exposed_sides += count_exposed_sides(lava_point, lava_grid)

print("Total exposed sides = ", total_exposed_sides)


# Iterate through a vector of trees in direction of viewing, marking true for those you can see from that direction
def is_inside_rock(lava_vec):
    if max(lava_vec, default=0) > 0:
        return True
    return False


# Part 2, now we need to ignore interior parts
# For each square in the grid, look in all directions. If all directions have a rock, you could be inside a rock
def could_location_be_inside_rock(x, y, z, lava_grid):
    if lava_grid[x,y,z] != 0: #Doesn't count as in rock if it is rock
        return False
    if not is_inside_rock(lava_grid[:x, y, z]):
        return False
    if not is_inside_rock(lava_grid[x:, y, z]):
        return False
    if not is_inside_rock(lava_grid[x, :y, z]):
        return False
    if not is_inside_rock(lava_grid[x, y:, z]):
        return False
    if not is_inside_rock(lava_grid[x, y, :z]):
        return False
    if not is_inside_rock(lava_grid[x, y, z:]):
        return False

    return True


# If a location is surrounded by no air, it stays as it is. If it has some air around it (that is not potentially inside the rock),
# it turns back into a 0 and is confirmed as outside the lava
# The return True or False is unrepresentative, it's just used to track if there has been a change
def is_location_still_potentially_in_rock(x, y, z, lava_grid):
    if lava_grid[x,y,z] != 2:
        return True
    if x > 0 and lava_grid[x-1,y,z] == 0:
        lava_grid[x,y,z] = 0
        return False
    if x < lava_grid.shape[0] and lava_grid[x+1,y,z] == 0:
        lava_grid[x, y, z] = 0
        return False
    if y > 0 and lava_grid[x, y-1, z] == 0:
        lava_grid[x, y, z] = 0
        return False
    if y < lava_grid.shape[1] and lava_grid[x, y+1, z] == 0:
        lava_grid[x, y, z] = 0
        return False
    if z > 0 and lava_grid[x, y, z-1] == 0:
        lava_grid[x, y, z] = 0
        return False
    if z < lava_grid.shape[2] and lava_grid[x, y, z+1] == 0:
        lava_grid[x, y, z] = 0
        return False
    return True

# Loop over points to find any potentially inside points
for x in range(0, lava_grid.shape[0]):
    for y in range(0, lava_grid.shape[1]):
        for z in range(0, lava_grid.shape[2]):
            if could_location_be_inside_rock(x, y, z, lava_grid):
                lava_grid[x,y,z] = 2
                # print("Found an inside value at", x, y, z)


# Iterate over points to check if they are surrounded by any air. If they are, they are confirmed as outside the rock.
# When no more elements change, the possibly in a rock segments turn into for sure in a rock segments.
removed_features = 1
while removed_features > 0:
    removed_features = 0
    for x in range(0, lava_grid.shape[0]):
        for y in range(0, lava_grid.shape[1]):
            for z in range(0, lava_grid.shape[2]):
                is_still_in_rock = is_location_still_potentially_in_rock(x,y,z,lava_grid)
                if not is_still_in_rock:
                    # print("Found a value that cannot be in a rock at:", x, y, z)
                    removed_features += 1


total_exposed_sides = 0
for lava_point in lava_coords:
    total_exposed_sides += count_exposed_sides(lava_point, lava_grid)

print("Total exposed sides when ignoring insides = ", total_exposed_sides)