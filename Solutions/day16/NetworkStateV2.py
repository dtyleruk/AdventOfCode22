import copy


class NetworkStateV2:
    def __init__(self, age, pressure, total_pressure, location, closed_valves, time_to_location):
        self.age = age
        self.pressure = pressure
        self.total_pressure = total_pressure
        self.location = location
        self.closed_valves = closed_valves
        self.time_to_location = time_to_location

    def create_next_steps(self, valve_distances, valve_pressures, max_age):

        self.age += 1
        self.total_pressure += self.pressure
        self.time_to_location -= 1

        # Bascially wait until we get there to do anything
        if self.time_to_location == 0:
            if self.location in valve_pressures:
                self.pressure += valve_pressures[self.location]

        if self.time_to_location >= 0:
            return [self]

        # TODO this is the part to move it finished states, if it's slow
        if len(self.closed_valves) == 0:
            return [self]

        new_states = []
        for next_location in self.closed_valves:
            travel_time = valve_distances[self.location][next_location]

            new_closed_valves = copy.deepcopy(self.closed_valves)
            new_closed_valves.remove(next_location)

            this_state = NetworkStateV2(self.age,
                                        self.pressure,
                                        self.total_pressure,
                                        next_location,
                                        new_closed_valves,
                                        travel_time)

            new_states.append(this_state)

        return new_states



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
        return "Age: " + str(self.age) + " Location: " + self.location + " Pres: " + str(self.pressure) + " TotPres: " + str(self.total_pressure) + " Time to location: " + str(self.time_to_location)


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

        self.states = new_states
        print("Age: ", self.age, " State count: ", len(self.states), " Finished state count: ", len(self.finished_states), " Max pressure: ", self.get_max_total_pressure())

    def run_all_steps(self):
        while self.age < self.max_age:
            self.add_step()

    def get_max_total_pressure(self):
        max_total_pressure = 0
        for state in self.states:
            if state.total_pressure > max_total_pressure:
                max_total_pressure = state.total_pressure
        for state in self.finished_states:
            if state.total_pressure > max_total_pressure:
                max_total_pressure = state.total_pressure
        return max_total_pressure
