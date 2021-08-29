
class Input:
    def __init__(self, name):
        self.name = name

    def size(self):
        return 1


class CurrentInput(Input):
    def __init__(self, name, current):
        Input.__init__(self, name)
        self.current = current


class PoissonInput(Input):
    def __init__(self, name, rate):
        Input.__init__(self, name)
        self.rate = rate

class SpikeToRate(Input):
    def __init__(self, name):
        Input.__init__(self, name)

class RateToSpike(Input):
    def __init__(self, name):
        Input.__init__(self, name)

