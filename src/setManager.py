class SetManager:

    def __init__(self):
        self.Sets = []

    def add_set(self, functionSet):
        self.Sets.append(functionSet)

    def get_by_name(self, name):
        for function in self.Sets:
            if function.getName() == name:
                return function
        return None
