import re
import copy

class Valve:
    def __init__(self, id, flow_rate):
        super().__init__()
        self.id = id
        self.flow_rate = flow_rate
        self.connections = []  # List of valves connecting this one
        self.connection_ids = []

    # Connects valves to another one. (Chose to not bother making it both ways, just because I'm lazy and the input is sanitized
    def add_connection(self, valve):
        self.connections.append(valve)
        self.connection_ids.append(valve.id)

    def __str__(self) -> str:
        return self.id + " " + str(self.flow_rate) + " " + self.connections_string()

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    def __hash__(self) -> int:
        return hash(self.id)

    def connections_string(self):
        string = "("
        for connection in self.connections:
            string += connection.id
            string += " "
        string += ")"

        return re.sub(",\)",")", re.sub(" ", ",", string))


class Network:
    def __init__(self, input_string):
        super().__init__()

        self.valves = []

        # First add all valves to network
        for input_line in input_string:
            id = input_line[6:8]
            flow_rate = int(re.findall("[0-9]+", input_line)[0])
            self.valves.append(Valve(id, flow_rate))

        # Now add connections
        for input_line in input_string:
            id = input_line[6:8]
            valve = self.get_valve_by_id(id)

            trimmed_input = re.sub("s", "", input_line)
            tunnel_info_start_index = re.search("tunnel lead to valve ", trimmed_input).start()

            tunnel_info = trimmed_input[(tunnel_info_start_index+len("tunnel lead to value ")):]
            tunnel_info = re.sub(" ","", tunnel_info)
            tunnels = re.split(",", tunnel_info)

            for tunnel_id in tunnels:
                tunnel_destination = self.get_valve_by_id(tunnel_id)
                valve.add_connection(tunnel_destination)

    def get_valve_by_id(self, valve_id):
        for valve in self.valves:
            if valve.id == valve_id:
                return valve


class NetworkStatus:
    def __init__(self, network: Network, age, total_pressure, unit_pressure, location, open_valves, previous_location):
        super().__init__()
        self.network = network

        self.age = age
        self.total_pressure = total_pressure
        self.unit_pressure = unit_pressure
        self.location = location
        self.open_valves = open_valves
        self.previous_location = previous_location

    def __str__(self) -> str:
        valves_string = "OpenValves: "
        for valve in self.open_valves:
            valves_string += valve.id
            valves_string += ","
        return "Age: " + str(self.age) + " TotPressure: " + str(self.total_pressure) + " Location: " + str(self.location.id) + " " + valves_string

    def __eq__(self, o: object) -> bool:
        return self.total_pressure == o.total_pressure and self.location.id == o.location.id and self.open_valves == o.open_valves

    def __hash__(self) -> int:
        return hash(self.age) + hash(self.total_pressure) + hash(self.location.id) + hash(tuple(self.open_valves))

    def open_valves_string(self):
        valve_string = ""
        for valve in self.open_valves:
            valve_string += valve.id
        return valve_string

    def add_pressure(self):
        self.total_pressure += self.unit_pressure

    def get_step_options(self, allow_open):
        step_options = []
        if not self.is_location_valve_open() and self.location.flow_rate > 0 and allow_open:
            step_options = ["Open"]
        for connection in self.location.connection_ids:
            if self.previous_location.id != connection:
                step_options.append(connection)
        return step_options

    def is_location_valve_open(self):
        for valve in self.open_valves:
            if valve.id == self.location.id:
                return True
        return False

    def create_next_steps(self, allow_open):
        step_options = self.get_step_options(allow_open)

        self.add_pressure()

        new_statuses = []
        new_age = self.age + 1

        for option in step_options:

            if option == "Open":
                new_open_valves = [self.location]
                new_open_valves.extend(self.open_valves)
                self.unit_pressure += self.location.flow_rate
                new_statuses.append(NetworkStatus(self.network, new_age,
                                                  self.total_pressure, self.unit_pressure, copy.deepcopy(self.location),
                                                  copy.deepcopy(new_open_valves), copy.deepcopy(self.location), ))

            else:
                new_location = self.network.get_valve_by_id(option)
                new_statuses.append(NetworkStatus(self.network, new_age, self.total_pressure, self.unit_pressure, new_location,
                                                  copy.deepcopy(self.open_valves), copy.deepcopy(self.location)))

        return new_statuses
