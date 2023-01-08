import copy
import re
import numpy as np


class RobotFactory:
    def __init__(self, input_string):
        values = list(map(int, re.findall('\d+', input_string)))

        self.age = 0

        self.id = values[0]

        # The 3 values correspond to ore, clay and obsidian
        self.ore_robot_cost = [values[1], 0, 0]
        self.clay_robot_cost = [values[2], 0, 0]
        self.obsidian_robot_cost = [values[3], values[4], 0]
        self.geode_robot_cost = [values[5], 0, values[6]]

    # There are 5 possible options, do nothing, or build each type of robot. Figure out which are possible
    # The options are:
    # 0-4 for do nothing, build ore robot, build clay robot, build obsidian robot, build geode robot
    def what_robots_can_be_built(self, material_counts):
        options = [True]
        options.append(material_counts[0] >= self.ore_robot_cost[0])
        options.append(material_counts[0] >= self.clay_robot_cost[0])
        options.append(
            material_counts[0] >= self.obsidian_robot_cost[0] and material_counts[1] >= self.obsidian_robot_cost[1])
        options.append(
            material_counts[0] >= self.obsidian_robot_cost[0] and material_counts[2] >= self.geode_robot_cost[2])
        return options


class RobotFactoryState:

    def __init__(self, robot_factory: RobotFactory, age, robot_counts, material_counts):
        self.robot_factory = robot_factory
        self.age = age
        # The 4 values correspond to ore, clay, obsidian and geode
        self.robot_counts = robot_counts
        self.material_counts = material_counts

    # Returns a list of new states for each option
    # Three steps, Determine what can be built
    # Gather resources
    # Build new robot
    def advance_one_min(self):
        next_step_options = self.robot_factory.what_robots_can_be_built(self.material_counts)
        self.gather_resources()
        return self.get_next_min_states(next_step_options)

    def gather_resources(self):
        self.material_counts += self.robot_counts

    def get_next_min_states(self, next_step_options):
        new_states = []
        if next_step_options[0]:
            new_states.append(RobotFactoryState(self.robot_factory, self.age + 1, self.robot_counts,
                                                self.material_counts))
        if next_step_options[1]:
            new_states.append(
                RobotFactoryState(self.robot_factory, self.age + 1, self.add_ore_robot(), self.pay_for_ore_robot()))
        if next_step_options[2]:
            new_states.append(
                RobotFactoryState(self.robot_factory, self.age + 1, self.add_clay_robot(), self.pay_for_clay_robot()))
        if next_step_options[3]:
            new_states.append(RobotFactoryState(self.robot_factory, self.age + 1, self.add_obsidian_robot(),
                                                self.pay_for_obsidian_robot()))
        if next_step_options[3]:
            new_states.append(
                RobotFactoryState(self.robot_factory, self.age + 1, self.add_geode_robot(), self.pay_for_geode_robot()))
        return new_states

    def add_ore_robot(self):
        return np.array((self.robot_counts[0] + 1, self.robot_counts[1], self.robot_counts[2], self.robot_counts[3]))

    def pay_for_ore_robot(self):
        return np.array((self.material_counts[0] - self.robot_factory.ore_robot_cost[0], self.material_counts[1], \
               self.material_counts[2], self.material_counts[3]))

    def add_clay_robot(self):
        return np.array((self.robot_counts[0], self.robot_counts[1] + 1, self.robot_counts[2], self.robot_counts[3]))

    def pay_for_clay_robot(self):
        return np.array((self.material_counts[0] - self.robot_factory.clay_robot_cost[0], self.material_counts[1], \
               self.material_counts[2], self.material_counts[3]))

    def add_obsidian_robot(self):
        return np.array((self.robot_counts[0], self.robot_counts[1], self.robot_counts[2] + 1, self.robot_counts[3]))

    def pay_for_obsidian_robot(self):
        return np.array((self.material_counts[0] - self.robot_factory.obsidian_robot_cost[0],
                self.material_counts[1] - self.robot_factory.obsidian_robot_cost[1],
                self.material_counts[2],
                self.material_counts[3]))

    def add_geode_robot(self):
        return np.array((self.robot_counts[0], self.robot_counts[1], self.robot_counts[2], self.robot_counts[3] + 1))

    def pay_for_geode_robot(self):
        return np.array((self.material_counts[0] - self.robot_factory.geode_robot_cost[0],
                self.material_counts[1],
                self.material_counts[2] - self.robot_factory.geode_robot_cost[2],
                self.material_counts[3]))

    # A state is deemed better if it has more than or equal to in each material and robot type
    def is_input_state_better(self, input_state):

        # # self.robot_counts.
        # if min(self.robot_counts <= input_state.robot_counts) and min(self.material_counts <= input_state.material_counts):
        #     return True
        # return False

        if (self.robot_counts[0] <= input_state.robot_counts[0] and
                self.robot_counts[1] <= input_state.robot_counts[1] and
                self.robot_counts[2] <= input_state.robot_counts[2] and
                self.robot_counts[3] <= input_state.robot_counts[3] and
                self.material_counts[0] <= input_state.material_counts[0] and
                self.material_counts[1] <= input_state.material_counts[1] and
                self.material_counts[2] <= input_state.material_counts[2] and
                self.material_counts[3] <= input_state.material_counts[3]):
            return True
        return False

    def __str__(self) -> str:
        return "Age: " + str(self.age) + " Mat counts: " + str(self.material_counts) + " Robot counts: " + str(
            self.robot_counts)
