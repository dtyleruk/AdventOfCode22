from Solutions.day16.Valve import NetworkStatus, Network
from Solutions.day16.NetworkStateV2 import NetworkStateV2, NetworkRunner

f = open("../../Inputs/day16/part1.dat", "r")
input = f.read().splitlines()


def take_step(network_states):
    new_network_states = set()
    for state in network_states:
        this_new_states = state.create_next_steps(False)
        for new_state in this_new_states:
            new_network_states.add(new_state)
    return new_network_states


# For each valve, calculate how long it takes to get to each other valve
def calc_valve_distances(network):

    valve_distances = {}

    # Need to calculate distance to other valves from this valve
    for valve in network.valves:
        print("PreProcessing valve:", valve.id)
        found_valves = {}

        init_state = NetworkStatus(network, 0, 0, 0, valve, set(), valve)
        states = [init_state]

        while len(found_valves) < (len(network.valves)):

            states = take_step(states)

            for state in states:
                if found_valves.get(state.location.id) is None:
                    found_valves.update({state.location.id: state.age})

        found_valves.pop(valve.id)

        to_pop = []
        for found_value in found_valves.keys():
            if network.get_valve_by_id(found_value).flow_rate == 0:
                to_pop.append(found_value)

        for valve_to_remove in to_pop:
            found_valves.pop(valve_to_remove)

        valve_distances.update({valve.id: found_valves})
    return valve_distances


network = Network(input)

initial_network_state = NetworkStatus(network, 0, 0, 0, network.get_valve_by_id("AA"), set(), network.get_valve_by_id("AA"))

network_states = [initial_network_state]


valve_distances = calc_valve_distances(network)
valve_pressures = {}
for valve in network.valves:
    if valve.flow_rate > 0:
        valve_pressures.update({valve.id: valve.flow_rate})

# Add one to account for the valve turn on time
def add_one_to_distances(valve_distances):
    for valve in valve_distances:
        for key in valve_distances[valve]:
            valve_distances[valve][key] += 1

add_one_to_distances(valve_distances)

init_network_v2 = NetworkStateV2(1, 0, 0, "AA", set(valve_pressures.keys()))

network_runner = NetworkRunner(valve_distances, valve_pressures, 31, init_network_v2)

network_runner.run_all_steps()


print("Max pressure is: ", network_runner.get_max_total_pressure())

belb = 1