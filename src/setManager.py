class SetManager:

    def __init__(self):
        self.Sets = []

    def add_set(self, function_set):
        self.Sets.append(function_set)

    def get_by_name(self, name):
        for function in self.Sets:
            if function.get_name() == name:
                return function
        return None
