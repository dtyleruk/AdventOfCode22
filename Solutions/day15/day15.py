from Solutions.day15.Sensor import Sensor
import numpy as np

f = open("../../Inputs/day15/part1.dat", "r")
# f = open("../../Inputs/day15/test_data.dat", "r")
input = f.read().splitlines()

sensors = []
for input_line in input:
    sensors.append(Sensor(input_line))

row_to_check = 2000000
# row_to_check = 10
blocked_elements = []
for sensor in sensors:
    this_blocked_elements = sensor.which_y_elements_of_row_x_cannot_contain_beacon(row_to_check)
    if this_blocked_elements is not None:
        blocked_elements.append(this_blocked_elements)

blocked_elements = np.array(blocked_elements)


# Now need to combine ranges to find final set
def combine_ranges(ranges):
    blocked_values = set()
    for this_range in ranges:
        for i in range(this_range[0], this_range[1] + 1):
            blocked_values.add(i)
    return blocked_values


invalid_range = combine_ranges(blocked_elements)

for sensor in sensors:
    if sensor.nearest_beacon.y == row_to_check:
        if invalid_range.__contains__(sensor.nearest_beacon.x):
            invalid_range.remove(sensor.nearest_beacon.x)

print("Size of invalid_range:", len(invalid_range))
belb = 1