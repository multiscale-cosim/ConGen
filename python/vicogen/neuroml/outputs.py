
class Output:
    def __init__(self, name):
        self.name = name

    def size(self):
        return 1


class Multimeter(Output):
    def __init__(self, name):
        Output.__init__(self, name)

class SpikeDetector(Output):
    def __init__(self, name):
        Output.__init__(self, name)
