import copy


class NetworkStateV2:
    def __init__(self, age, pressure, total_pressure, location_1, location_2, time_to_location_1, time_to_location_2, closed_valves):
        self.age = age
        self.pressure = pressure
        self.total_pressure = total_pressure
        self.location_1 = location_1
        self.location_2 = location_2
        self.closed_valves = closed_valves
        self.time_to_location_1 = time_to_location_1
        self.time_to_location_2 = time_to_location_2

    def create_next_steps(self, valve_distances, valve_pressures, max_age):

        self.age += 1
        self.total_pressure += self.pressure
        self.time_to_location_1 -= 1
        self.time_to_location_2 -= 1

        # Bascially wait until we get there to do anything
        if self.time_to_location_1 == 0:
            if self.location_1 in valve_pressures:
                self.pressure += valve_pressures[self.location_1]

        if self.time_to_location_2 == 0:
            if self.location_2 in valve_pressures:
                self.pressure += valve_pressures[self.location_2]

        if self.time_to_location_1 >= 0 and self.time_to_location_2 >= 0:
            return [self]

        # TODO this is the part to move it finished states, if it's slow
        if len(self.closed_valves) == 0:
            return [self]

        new_states = []
        if self.time_to_location_1 < 0:

            for next_location in self.closed_valves:
                travel_time = valve_distances[self.location_1][next_location]

                new_closed_valves = copy.deepcopy(self.closed_valves)
                new_closed_valves.remove(next_location)

                this_state = NetworkStateV2(self.age,
                                            self.pressure,
                                            self.total_pressure,
                                            next_location,
                                            self.location_2,
                                            travel_time,
                                            self.time_to_location_2,
                                            new_closed_valves
                                            )

                new_states.append(this_state)

        if self.time_to_location_2 < 0:

            if len(new_states) == 0:
                # Do the same as for location 1, copy paste because it's late
                for next_location in self.closed_valves:
                    travel_time = valve_distances[self.location_2][next_location]

                    new_closed_valves = copy.deepcopy(self.closed_valves)
                    new_closed_valves.remove(next_location)

                    this_state = NetworkStateV2(self.age,
                                                self.pressure,
                                                self.total_pressure,
                                                self.location_1,
                                                next_location,
                                                self.time_to_location_2,
                                                travel_time,
                                                new_closed_valves
                                                )

                    new_states.append(this_state)

            else:
                # Now need to do this for each of the new_states
                new_new_states = []
                for state in new_states:
                    for next_location in state.closed_valves:

                        travel_time = valve_distances[state.location_2][next_location]

                        new_closed_valves = copy.deepcopy(state.closed_valves)
                        new_closed_valves.remove(next_location)

                        this_state = NetworkStateV2(state.age,
                                                    state.pressure,
                                                    state.total_pressure,
                                                    state.location_1,
                                                    next_location,
                                                    state.time_to_location_1,
                                                    travel_time,
                                                    new_closed_valves
                                                    )

                        new_new_states.append(this_state)

                return prune_new_new_states(new_new_states)

        return new_states

    def get_prune_key_to_remove_bad_tot_pressure(self):
        return (str(self.closed_valves), self.location_1, self.location_2, self.time_to_location_1, self.time_to_location_2, self.pressure)

    def get_prune_key_to_remove_behind(self):
        return (str(self.closed_valves), self.location_1, self.location_2,self.pressure)

    # Stops adding pressure at max time
    def calc_added_pressure(self, max_age, travel_time):
        if self.age + travel_time <= max_age:
            return travel_time * self.pressure
        else:
            return (max_age - self.age) * travel_time

    # Assuming constant rate of pressure, add pressure until time
    def add_pressure_to_time(self, max_age):
        time_to_max = max_age - self.age
        self.age += time_to_max
        self.total_pressure += time_to_max * self.pressure

    def __str__(self) -> str:
        return "Age: " + str(self.age) + " Locations: (" + self.location_1 + "," + self.location_2 + ") Pres: " + str(self.pressure) + " TotPres: " + str(self.total_pressure) + " Time to locations: (" + str(self.time_to_location_1) + "," + str(self.time_to_location_2) + ")"


# Function to remove duplicate states due to locations being symetric
def prune_new_new_states(new_states):
    locations_searched = []

    states_to_keep = []
    for state in new_states:
        if (state.location_2, state.location_1) not in locations_searched:
            states_to_keep.append(state)
            locations_searched.append((state.location_1, state.location_2))

    return states_to_keep

def prune_symetric_states(states):
    states_to_keep = {}
    for state in states:
        prune_key = (str(state.closed_valves), state.location_2, state.location_1, state.time_to_location_2, state.time_to_location_1, state.pressure, state.total_pressure)
        if prune_key not in states_to_keep:
            prune_key_to_add = (str(state.closed_valves), state.location_1, state.location_2, state.time_to_location_1, state.time_to_location_2, state.pressure, state.total_pressure)
            states_to_keep.update({prune_key_to_add: state})
        else:
            belb = 1 #Do nothn

    print("prune_symetric_states all states: ", len(states), " pruned states:", len(states_to_keep))
    return list(states_to_keep.values())

# Function to weed out inferior states
def prune_states(states):
    states_to_keep = {}
    for state in states:
        prune_key = state.get_prune_key_to_remove_bad_tot_pressure()
        if prune_key not in states_to_keep:
            states_to_keep.update({prune_key: state})
        else:
            if state.total_pressure > states_to_keep[prune_key].total_pressure:
                states_to_keep.update({prune_key: state})

    print("Len of all states: ", len(states), " Len of pruned states:", len(states_to_keep.values()))
    states = list(states_to_keep.values())
    states = prune_states_remove_behind(states)
    return states
    # return prune_symetric_states(states)

def prune_states_remove_behind(states):
    states_to_keep = {}
    for state in states:
        prune_key = state.get_prune_key_to_remove_behind()
        if prune_key not in states_to_keep:
            big_prune_key = state.get_prune_key_to_remove_bad_tot_pressure()
            states_to_keep.update({prune_key: {big_prune_key: state}})
        else:
            comparison_states = states_to_keep[prune_key]
            new_comparison_states = {}
            for key in comparison_states:
                this_comparison = comparison_states[key]
                if state.total_pressure > this_comparison.total_pressure and state.time_to_location_1 <= this_comparison.time_to_location_1 and state.time_to_location_2 <= this_comparison.time_to_location_2:
                    belb = 1  # Do nothing
                if this_comparison.total_pressure > state.total_pressure and this_comparison.time_to_location_1 <= state.time_to_location_1 and this_comparison.time_to_location_2 <= state.time_to_location_2:
                    new_comparison_states = comparison_states
                    break
                else:
                    new_comparison_states.update({key: this_comparison})
            states_to_keep.update({prune_key: new_comparison_states})

    states_to_keep_list = []
    for small_prune in states_to_keep:
        this_one = states_to_keep[small_prune]
        for big_prune in this_one:
            states_to_keep_list.append(this_one[big_prune])


    print("Len of all states: ", len(states), " Len of pruned remove_behind states:", len(states_to_keep_list))
    return states_to_keep_list




class NetworkRunner:
    def __init__(self, valve_distances, valve_pressures, max_age, init_network_state:NetworkStateV2):
        self.max_age = max_age
        self.age = 0
        self.states = [init_network_state]
        self.valve_distances = valve_distances
        self.valve_pressures = valve_pressures
        self.finished_states = []

    def add_step(self):
        self.age += 1
        new_states = []
        for state in self.states:
            states_to_add = state.create_next_steps(self.valve_distances, self.valve_pressures, self.max_age)
            new_states.extend(states_to_add)  # Eff gain, give each network a subset of valves

        new_states = prune_states(new_states)

        self.states = new_states
        print("Age: ", self.age, " State count: ", len(self.states), " Finished state count: ", len(self.finished_states), " Max pressure: ", self.get_max_total_pressure())

    # iterate over all states, only keep top n total_pressures, might work
    def keep_top_n_results(self, n):
        if n > len(self.states):
            return

        curr_pressures = []
        for state in self.states:
            curr_pressures.append(state.total_pressure)
        curr_pressures.sort(reverse=True)
        cut_off_pressure = curr_pressures[n]
        states_to_keep = []
        for state in self.states:
            if state.total_pressure >= cut_off_pressure:
                states_to_keep.append(state)
        self.states = states_to_keep

    def run_all_steps(self):
        while self.age < self.max_age:
            self.add_step()
            self.keep_top_n_results(50000)

    def get_max_total_pressure(self):
        max_total_pressure = 0
        for state in self.states:
            if state.total_pressure > max_total_pressure:
                max_total_pressure = state.total_pressure
        for state in self.finished_states:
            if state.total_pressure > max_total_pressure:
                max_total_pressure = state.total_pressure
        return max_total_pressure
