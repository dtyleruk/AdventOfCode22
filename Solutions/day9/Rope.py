class Rope:

    def __init__(self, input_string, rope_length):
        super().__init__()
        self.knots = []
        for i in range(0, rope_length):
            self.knots.append((0, 0))

        self.tail_locations = set()
        self.tail_locations.add((0, 0))

        self.instructions = []
        for instruction_string in input_string:
            self.instructions.append(Instruction(instruction_string))

    def squares_tail_has_been_in(self):
        return len(self.tail_locations)

    def run_all_moves(self):
        for instruction in self.instructions:
            self.run_one_instruction(instruction)

    def run_one_instruction(self, instruction):
        for i in range(0, instruction.distance):
            # First move head
            self.run_one_move(instruction.move_vector)

    def run_one_move(self, move_vector):
        # First move head
        self.knots[0] = add_coordinates(self.knots[0], move_vector)

        for knot_to_move in range(1, len(self.knots)):
            # Then determine if next knot needs to move
            self.move_next_knot(knot_to_move)
            # Then add tail location to

        self.tail_locations.add(self.knots[len(self.knots)-1])

    def move_next_knot(self, knot_to_move_index):
        gap_from_tail_to_head = distance_to_coordinate(self.knots[knot_to_move_index], self.knots[knot_to_move_index-1])
        abs_distance_from_tail_to_head = abs(gap_from_tail_to_head[0]), abs(gap_from_tail_to_head[1])
        if max(abs_distance_from_tail_to_head) <= 1:  # Head and tail are touching, so the tail doesn't need to move
            return
        # If tail moves, the new gap must be (pm1,0) or (0, pm1)
        # Each element of gap_from_tail_to_head that is greater than 0 need to get one closer to 0
        total_distance_from_tail_to_head = sum(abs_distance_from_tail_to_head)

        # Here the map is: -2,-1,0,1,2 -> -1,0,0,0,1
        if total_distance_from_tail_to_head == 2:
            move_tail_by = divide_tuple_by(gap_from_tail_to_head, 3)
        # Here the map is -2,-1,0,1,2 -> -1,-1,0,1,1
        else:
            move_tail_by = divide_tuple_by(gap_from_tail_to_head, 1.9)

        self.knots[knot_to_move_index] = add_coordinates(self.knots[knot_to_move_index], move_tail_by)


class Instruction:
    def __init__(self, input_string):
        super().__init__()
        self.direction = input_string[0]
        self.distance = int(input_string[2:])
        self.move_vector = get_move_vector(self.direction)


def add_coordinates(x1, x2):
    return (x1[0] + x2[0], x1[1] + x2[1])


# x2 - x1, or how to move from x1 to x2
def distance_to_coordinate(x1, x2):
    return (x2[0] - x1[0], x2[1] - x1[1])


def divide_tuple_by(tuple, x):
    return (round(tuple[0]/x), round(tuple[1]/x))


def get_move_vector(direction):
    if direction == "U":
        return (0, -1)
    if direction == "D":
        return (0, 1)
    if direction == "L":
        return (-1, 0)
    if direction == "R":
        return (1 ,0)
    # pppfft, who needs error handling?
