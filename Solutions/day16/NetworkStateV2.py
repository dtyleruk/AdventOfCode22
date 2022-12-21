import copy


class NetworkStateV2:
    def __init__(self, age, pressure, total_pressure, location, closed_valves):
        self.age = age
        self.pressure = pressure
        self.total_pressure = total_pressure
        self.location = location
        self.closed_valves = closed_valves

    def create_next_steps(self, valve_distances, valve_pressures, max_age):
        new_states = []

        for next_location in self.closed_valves:
            travel_time = valve_distances[self.location][next_location]

            added_pressure = self.calc_added_pressure(max_age, travel_time)

            new_closed_valves = copy.deepcopy(self.closed_valves)
            new_closed_valves.remove(next_location)

            this_state = NetworkStateV2(self.age + travel_time,
                                        self.pressure + valve_pressures[next_location],
                                        self.total_pressure + added_pressure,
                                        next_location,
                                        new_closed_valves)

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
        return "Age: " + str(self.age) + " Location: " + self.location + " Pres: " + str(self.pressure) + " TotPres: " + str(self.total_pressure)


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
            if state.age <= self.age:
                states_to_add = state.create_next_steps(self.valve_distances, self.valve_pressures, self.max_age)
                if len(states_to_add) > 0:
                    new_states.extend(states_to_add)  # Eff gain, give each network a subset of valves
                else:
                    state.add_pressure_to_time(self.max_age)
                    new_states.append(state)
            else:
                new_states.append(state)
        self.states = new_states
        print("Age: ", self.age, " State count: ", len(self.states))

    def run_all_steps(self):
        while self.age < self.max_age:
            self.add_step()

    def get_max_total_pressure(self):
        max_total_pressure = 0
        for state in self.states:
            if state.total_pressure > max_total_pressure:
                max_total_pressure = state.total_pressure
        return max_total_pressure
