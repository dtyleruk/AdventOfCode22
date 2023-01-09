import numpy as np
import re

from Solutions.day19.RobotFactory import RobotFactory, RobotFactoryState

f = open("../../Inputs/day19/part1.dat", "r")
input = f.read().splitlines()

test = re.findall('\d+', input[0])

robot_factories = []

for line in input:
    robot_factories.append(RobotFactory(line))

def is_robot_count_b_better_than_a(a,b):
    # return a != b and (a[0] <= b[0] and
    #             a[1] <= b[1] and
    #             a[2] <= b[2] and
    #             a[3] <= b[3])
    return (a[0] <= b[0] and
                a[1] <= b[1] and
                a[2] <= b[2] and
                a[3] <= b[3])

def prune_states_that_cant_catch_max_geode_count(states, time_remaining):
    # Step 0.5, see which states have no chance of catching up.

    max_geodes = 0
    for state in states:
        if state.material_counts[3] + state.robot_counts[3] * time_remaining > max_geodes:
            max_geodes = state.material_counts[3] + state.robot_counts[3] * time_remaining

    print("Starting with ", len(states), " states for catch_max_geode pruning, time_remaining = ", time_remaining, ", max_geodes = ", max_geodes)

    if max_geodes == 0:
        print("No geodes found")
        return states

    to_remove = set()

    for state_index in range(0, len(states)):
        if states[state_index].theoretical_max_geodes(time_remaining) < max_geodes:
            to_remove.add(state_index)

    if len(to_remove) > 0:
        print("Removing ", len(to_remove), " states")
        to_remove = sorted(list(to_remove))
        for loop_state in reversed(to_remove):
            del states[loop_state]
    print("Ended with ", len(states), " states for catch_max_geode pruning")

    return states


def prune_states(states, time_remaining):

    states = prune_states_that_cant_catch_max_geode_count(states, time_remaining)

    print("Pruning states")
    to_remove_attempt_2 = set()

    # Step one, build a dictionary of all robot counts, each will contain a list of material counts
    state_dictionary = dict()

    for state in states:
        if state_dictionary.get(state.robot_counts) is None:
            state_dictionary[state.robot_counts] = set()
        state_dictionary[state.robot_counts].add(state.material_counts)

    # Step one point 5, loop through dictionary and kick out already inferior cases
    # for state in state_dictionary:

    # Step two, loop through all states and only check the appropriate dictionary element
    for state_check_index in range(0, len(states)):
        for key in state_dictionary.keys():
            if is_robot_count_b_better_than_a(states[state_check_index].robot_counts, key):
                for material_count in state_dictionary[key]:
                    if is_robot_count_b_better_than_a(states[state_check_index].material_counts, material_count):
                        if states[state_check_index].material_counts == material_count and states[state_check_index].robot_counts == key:
                            pass
                        else:
                            to_remove_attempt_2.add(state_check_index)
                        break

    # Step three, remove repeated elements?
    to_remove = to_remove_attempt_2
    # # Slow and simple pruning method
    # print("Pruning states")
    # to_remove = set()
    #
    # for state_check_index in range(0, len(states)):
    #     for loop_state in range(0, len(states)):
    #         if loop_state == state_check_index:
    #             pass
    #         elif states[state_check_index].is_input_state_better(states[loop_state]):
    #             to_remove.add(state_check_index)
    #             break

    # Now actually remove them
    if len(to_remove) > 0:
        print("Removing ", len(to_remove), " states")
        to_remove = sorted(list(to_remove))
        for loop_state in reversed(to_remove):
            del states[loop_state]

    print("Done Pruning. Pruning removed: ", len(to_remove), " states to leave", len(states), "states")

    return states


def find_max_geodes_of_blueprint(init_state):
    time_passed = 0
    latest_states = [init_state]
    max_time = 24
    while time_passed < max_time:
        new_latest_states = []
        for state in latest_states:
            new_latest_states += state.advance_one_min()
        time_passed += 1
        latest_states = new_latest_states
        latest_states = prune_states(latest_states, max_time - time_passed)
        print("After ", time_passed, " mins, there are: ", len(latest_states), " states")

    print("Max geode count is:", latest_states[0].material_counts[3])
    return latest_states[0].material_counts[3]


quality_levels = []
quality_level_sum = 0

for blueprint in robot_factories:
    print("Running blueprint number:", blueprint.id)
    init_state = RobotFactoryState(blueprint, 0, (1, 0, 0, 0), (0, 0, 0, 0))
    max_geodes = find_max_geodes_of_blueprint(init_state)
    quality_levels.append(max_geodes * blueprint.id)
    quality_level_sum += max_geodes * blueprint.id

print("Total quality level: ", quality_level_sum)