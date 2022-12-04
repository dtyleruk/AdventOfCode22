import re


class AssignmentPair:
    def __init__(self, input_string):
        each_ass = re.split(',', input_string)
        self.ass1 = extract_assignment_values(each_ass[0])
        self.ass2 = extract_assignment_values(each_ass[1])

    def does_one_assignment_range_fully_contain_other(self):
        if does_ass1_fully_contain_ass2(self.ass1, self.ass2):
            return True
        if does_ass1_fully_contain_ass2(self.ass2, self.ass1):
            return True
        return False

    def do_assignemnts_overlap(self):
        if self.ass1[1] >= self.ass2[0] and self.ass1[0] <= self.ass2[1]:
            return True
        return False


# Make list of integers from input string in format 'int-int'
def extract_assignment_values(assignment_string):
    return [int(x) for x in re.split('-', assignment_string)]


def does_ass1_fully_contain_ass2(ass1, ass2):
    if ass1[0] <= ass2[0] and ass1[1] >= ass2[1]:
        return True
    return False

