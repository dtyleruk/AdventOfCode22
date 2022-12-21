from Solutions.day16.Valve import NetworkStatus, Network

f = open("../../Inputs/day16/part1.dat", "r")
input = f.read().splitlines()

network = Network(input)

initial_network_state = NetworkStatus(network, 0, 0, 0, network.get_valve_by_id("AA"), set(), network.get_valve_by_id("AA"))

network_states = [initial_network_state]


def take_step(network_states):
    new_network_states = set()
    for state in network_states:
        this_new_states = state.create_next_steps(True)
        for new_state in this_new_states:
            new_network_states.add(new_state)
    return new_network_states

def prune_states(network_states):

    tot_pressure_map = {}
    to_pop = []

    for state in network_states:
        state_string = state.location.id + "-" + state.open_valves_string()
        if tot_pressure_map.get(state_string) != None:
            if tot_pressure_map.get(state_string) < state.total_pressure:
                tot_pressure_map.update({state_string: state.total_pressure})
        else:
            tot_pressure_map.update({state_string: state.total_pressure})

    for state in set(network_states):
        state_string = state.location.id + "-" + state.open_valves_string()
        if tot_pressure_map[state_string] > state.total_pressure:
            network_states.remove(state)

    return network_states




# network_states = take_step(network_states)
# network_states = take_step(network_states)
# network_states = take_step(network_states)

for i in range(0, 30):
    print("Taking step ", i)
    print("There are currently: ", len(network_states), " network statues")
    network_states = take_step(network_states)
    pruned_network_states = prune_states(network_states)
    belb = 1

max_pressure = 0



for status in network_states:
    if status.total_pressure > max_pressure:
        max_pressure = status.total_pressure

print("Max total pressure is: ", max_pressure)