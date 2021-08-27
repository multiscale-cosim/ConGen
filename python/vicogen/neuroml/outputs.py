
class output:
    def __init__(self, name):
        self.name = name

    def size(self):
        return 1


class Monitor(Output):
    def __init__(self, name):
        Output.__init__(self, name)
