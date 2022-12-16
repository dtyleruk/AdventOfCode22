class InputPair:
    def __init__(self, list1, list2):
        super().__init__()
        self.list1 = list1
        self.list2 = list2
        self.in_order = None

    def are_lists_in_correct_order(self):
        for index in range(0, min(len(self.list1), len(self.list2))):
            this_comparison_result = self.compare_elements(self.list1[index], self.list2[index])
            if this_comparison_result is not None:
                return this_comparison_result
        if len(self.list1) < len(self.list2):
            return True
        elif len(self.list1) > len(self.list2):
            return False
        return None

    def compare_elements(self, lhs, rhs):
        if type(lhs) == type(rhs) == int:
            if lhs < rhs:
                return True
            elif lhs > rhs:
                return False
            else:
                return None
        #Otherwise, recurse
        elif type(lhs) == int and type(rhs) == list:
            new_pair = InputPair([lhs], rhs)
        elif type(lhs) == list and type(rhs) == int:
            new_pair = InputPair(lhs, [rhs])
        else:
            new_pair = InputPair(lhs, rhs)
        return new_pair.are_lists_in_correct_order()
