import numpy as np
import re

from Solutions.day19.RobotFactory import RobotFactory, RobotFactoryState

f = open("../../Inputs/day19/test_data.dat", "r")
input = f.read().splitlines()

test = re.findall('\d+', input[0])

robot_factories = []

for line in input:
    robot_factories.append(RobotFactory(line))


init_state = RobotFactoryState(robot_factories[0], 0, np.array((1, 0, 0, 0)), np.array((0, 0, 0, 0)))

time_passed = 0
latest_states = [init_state]

def prune_states(states):

    print("Pruning states")
    to_remove = set()

    for state_check_index in range(0, len(states)):
        for loop_state in range(0, len(states)):
            if loop_state == state_check_index:
                pass
            elif states[state_check_index].is_input_state_better(states[loop_state]):
                to_remove.add(state_check_index)
                break

    if len(to_remove) > 0:
        print("Removing ", len(to_remove), " states")
        to_remove = sorted(list(to_remove))
        for loop_state in reversed(to_remove):
            del states[loop_state]
    print("Done pruning states")
    return states






while time_passed < 24:
    new_latest_states = []
    for state in latest_states:
        new_latest_states += state.advance_one_min()
    time_passed += 1
    latest_states = new_latest_states
    latest_states = prune_states(latest_states)
    print("After ", time_passed, " mins, there are: ", len(latest_states), " states")

belb = 1