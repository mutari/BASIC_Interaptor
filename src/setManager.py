class SetManager:

    def __init__(self):
        self.Sets = []

    def addSet(self, functionSet):
        self.Sets.append(functionSet)

    def getByName(self, name):
        for function in self.Sets:
            if function.getName() == name:
                return function
        return None