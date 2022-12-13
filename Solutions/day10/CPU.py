class CPU:
    def __init__(self, instructions, first_poll, screen_width):
        super().__init__()
        self.age = 0
        self.X = 1
        self.instructions = []
        self.time_to_poll = first_poll
        self.poll_interval = screen_width
        self.poll_mult = first_poll
        self.poll_sum = 0
        self.x_poll_values = []

        self.render = [""]

        for instruction in instructions:
            self.instructions.append(parse_instruction(instruction))

    def run_instructions(self):
        for instruction in self.instructions:
            self.run_single_instruction(instruction)

    def run_single_instruction(self, instruction):
        run_time = instruction.age
        while run_time > 0:
            run_time -= 1
            self.time_to_poll -= 1
            if abs(self.age - self.X) < 2:
                char = "#"
            else :
                char = "."
            self.render[len(self.render)-1] += char
            self.age += 1
            if self.time_to_poll <= 0:
                self.render.append("")
                self.time_to_poll += self.poll_interval
                self.x_poll_values.append(self.X)
                self.poll_sum += self.poll_mult * self.X
                self.poll_mult += self.poll_interval
                self.age = 0 # This, like a lot of this day's solution is a wonky way to get part 2.
        instruction.perform_instruction(self)

    def render_output(self):
        for line in self.render:
            print(line)

def parse_instruction(instruction_string):
    if instruction_string == "noop":
        return Noop()
    if instruction_string[:4] == "addx":
        return AddX(int(instruction_string[5:]))


class Noop:
    def __init__(self) -> None:
        super().__init__()
        self.age = 1
        self.name = "noop"

    def perform_instruction(self, cpu):
        return


class AddX:
    def __init__(self, to_add):
        super().__init__()
        self.age = 2
        self.to_add = to_add
        self.name = "addX"

    def perform_instruction(self, cpu):
        cpu.X += self.to_add
        return
