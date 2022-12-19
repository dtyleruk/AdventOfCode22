import re

class Valve:
    def __init__(self, id, flow_rate):
        super().__init__()
        self.id = id
        self.flow_rate = flow_rate
        self.connections = []  # List of valves connecting this one

    # Connects valves to another one. (Chose to not bother making it both ways, just because I'm lazy and the input is sanitized
    def add_connection(self, valve):
        self.connections.append(valve)
        # valve.connections.add(self.connections)

    def __str__(self) -> str:
        return self.id + " " + str(self.flow_rate) + " " + self.connections_string()

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

    def get_valve_by_id(self, id):
        for valve in self.valves:
            if valve.id == id:
                return valve
