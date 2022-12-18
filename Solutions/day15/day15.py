from Solutions.day15.Sensor import Sensor
import numpy as np

f = open("../../Inputs/day15/part1.dat", "r")
# f = open("../../Inputs/day15/test_data.dat", "r")
input = f.read().splitlines()

sensors = []
for input_line in input:
    sensors.append(Sensor(input_line))


def calc_blocked_elements(row_to_check):

    blocked_elements = []
    for sensor in sensors:
        this_blocked_elements = sensor.which_y_elements_of_row_x_cannot_contain_beacon(row_to_check)
        if this_blocked_elements is not None:
            blocked_elements.append(this_blocked_elements)

    return np.array(blocked_elements)


# Combine a set of ranges into a list of elements, used in part 1 to count how many blocked spots there are
def combine_ranges(ranges):
    blocked_values = set()
    for this_range in ranges:
        for i in range(this_range[0], this_range[1] + 1):
            blocked_values.add(i)
    return blocked_values


# Part 2, need to find only possible location of hidden beacon
def get_valid_hidden_beacon_spots(ranges, row):
    if row % 1e5 == 0:
        print("Checking row:", row)
    # Sort blocked ranges from each sensor.
    # Ensure that the ranges overlap. If any don't, we have found a spot for the hidden beacon
    sorted_ranges = np.sort(ranges, axis=0)

    for i in range(1, np.shape(sorted_ranges)[0]):
        if sorted_ranges[i-1, 1] < sorted_ranges[i, 0]:
            return(sorted_ranges[i-1, 1] + 1, row)

    return None


# Part 1, check single row
row_to_check = 2000000
# row_to_check = 10
blocked_elements = calc_blocked_elements(row_to_check)
invalid_range = combine_ranges(blocked_elements)

# Boot out existing beacons
for sensor in sensors:
    if sensor.nearest_beacon.y == row_to_check:
        if invalid_range.__contains__(sensor.nearest_beacon.x):
            invalid_range.remove(sensor.nearest_beacon.x)

print("Size of invalid_range:", len(invalid_range))

max_row_to_check = 4000000
cheaty_start = 0  # 3300000

for row_to_check in range(cheaty_start, max_row_to_check):

    blocked_elements = calc_blocked_elements(row_to_check)

    any_valid_spots = get_valid_hidden_beacon_spots(blocked_elements, row_to_check)
    if any_valid_spots is not None:
        print("Valid spot for hidden beacon found at: ", any_valid_spots)
        print("Tuning frequency is:", int(any_valid_spots[0]) * 4000000 + int(any_valid_spots[1]))
        break
