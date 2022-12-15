import re
import math

# input_string is in the format:
# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3
class MonkeyGroup:
    def __init__(self, input_string, worry_divider):
        super().__init__()
        self.monkeys = []
        self.divisors = []
        for line in range(0, len(input_string), 7):
            self.monkeys.append(Monkey(input_string[line:(line + 6)], worry_divider, self))

        for monkey in self.monkeys:
            self.divisors.append(monkey.test.divisible_by)

        for monkey in self.monkeys:
            monkey.set_items()

    def perform_n_rounds(self, n):
        for round in range(0, n):
            self.perform_round()
            # print("Done round: ", round)

    def perform_round(self):
        for monkey in self.monkeys:
            monkey.inspect_items()

    def calc_monkey_business(self):
        active_monkeys = self.get_two_most_active_monkeys()
        return active_monkeys[0] * active_monkeys[1]

    def get_two_most_active_monkeys(self):
        monkey_inspection_counts = []
        for monkey in self.monkeys:
            monkey_inspection_counts.append(monkey.inspection_count)
        monkey_inspection_counts.sort(reverse=True)
        return monkey_inspection_counts[:2]

    def is_divisible_by_all(self, x):
        for monkey in self.monkeys:
            if not monkey.test.is_divisible_by(x):
                return False
        return True

class Monkey:
    def __init__(self, input_string, worry_divider, group: MonkeyGroup):
        super().__init__()
        self.group = group
        self.id = int(re.findall('\d+', input_string[0])[0])
        self.items = []
        self.operation = MonkeyOperation(input_string[2])
        self.test = MonkeyTest(input_string[3:])
        self.inspection_count = 0
        self.worry_divider = worry_divider

        init_values = [int(x) for x in re.findall('\d+', input_string[1])]
        for init_value in init_values:
            self.items.append(Item(self.group, init_value))


    def inspect_items(self):
        # print(self.items)
        for item in self.items:
            item = self.operation.apply_operation(item)
            item = math.floor(item/float(self.worry_divider))
            # to_throw_to = self.test.throw_to(item, self.id)
            self.throw_item(item, to_throw_to)
            self.inspection_count += 1
        self.items = []  # All items are thrown, so now we can clear them.
        # Hit a fun one here. I initially tried removing them as I iterated through the items,
        # but Python looks at the items list at the start of each iteration, so it all goes wrong
        # very quickly

    # Sets init remainder values of items
    def set_items(self):
        for item in self.items:
            item.set_item()


    def throw_item(self, item, throw_to):
        self.group.monkeys[throw_to].items.append(item)


class MonkeyTest:
    def __init__(self, input_string):
        super().__init__()
        self.divisible_by = int(re.findall('\d+', input_string[0])[0])
        self.true_throw_to = int(re.findall('\d+', input_string[1])[0])
        self.false_throw_to = int(re.findall('\d+', input_string[2])[0])

    def throw_to(self, x, id):
        if x.remainders[id] == 0:
            return self.true_throw_to
        return self.false_throw_to

    def is_divisible_by(self, x):
        if x % self.divisible_by == 0:
            return True
        return False


class MonkeyOperation:
    def __init__(self, input_string):
        super().__init__()
        strip_op = re.sub("Operation: new = ", "", input_string)
        split_by_space = re.split(" ", strip_op)
        self.part1 = split_by_space[2]
        self.operation = split_by_space[3]
        self.part2 = split_by_space[4]

    def part_value(self, x, part):
        if part == "old":
            return x
        return int(part)

    def part1_value(self, x):
        return self.part_value(x, self.part1)

    def part2_value(self, x):
        return self.part_value(x, self.part2)

    def apply_operation(self, x):
        if self.operation == "+":
            for i in range(0,len(x.remainders)):
                x.remainders[i] = self.part1_value(x.remainders[i]) + self.part2_value(x.remainders[i])
        elif self.operation == "*":
            for i in range(0,len(x.remainders)):
                x.remainders[i] = self.part1_value(x.remainders[i]) * self.part2_value(x.remainders[i])
        else:
            raise Exception("Unknown operation:", self.operation)
        for i in range(0, len(x.remainders)):
            x.remainders[i] = x.remainders[i] % x.group.divisors[i]
        return x


class Item:
    def __init__(self, group, init_value):
        self.group = group
        self.init_value = init_value
        self.remainders = []

    def set_item(self):
        for divisor in self.group.divisors:
            self.remainders.append(self.init_value % divisor)



