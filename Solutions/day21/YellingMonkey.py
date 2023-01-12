import re


class YellingMonkey:

    def __init__(self, input_string, monkey_dict):
        self.name = input_string[:4]
        self.monkey_dict = monkey_dict
        value = re.findall('\d+', input_string)

        if value == []:
            self.value = None
            self.parent1 = input_string[6:10]
            self.operation = input_string[11:12]
            self.parent2 = input_string[13:]
        else:
            self.value = int(value[0])
            self.parent1 = None
            self.operation = None
            self.parent2 = None

    def calc_value(self):
        if self.value is not None:
            return self.value

        if self.monkey_dict[self.parent1].value is None:
            self.monkey_dict[self.parent1].calc_value()
        if self.monkey_dict[self.parent2].value is None:
            self.monkey_dict[self.parent2].calc_value()

        self.value = self.perform_operation()

    def perform_operation(self):
        value = self.monkey_dict[self.parent1].value
        if self.operation == "+":
            return value + self.monkey_dict[self.parent2].value
        elif self.operation == "-":
            return value - self.monkey_dict[self.parent2].value
        elif self.operation == "*":
            return value * self.monkey_dict[self.parent2].value
        elif self.operation == "/":
            return value / self.monkey_dict[self.parent2].value
        else:
            raise Exception

    def __str__(self) -> str:
        string_val = self.name + " Value: " + str(self.value)
        if self.parent1 is not None:
            string_val += " Operation: " + str(self.parent1) + str(self.operation) + str(self.parent2)
        return string_val

