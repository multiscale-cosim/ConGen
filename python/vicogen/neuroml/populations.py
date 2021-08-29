import csa


class Population:
    def __init__(self, name, cell_type):
        """

        :param name: Identifier of the population
        :type name: str
        :param cell_type: cell type that is shared by all neurons in this population
        :type cell_type: str
        """
        self.name = name
        self.cell_type = cell_type

    def __repr__(self):
        return "%s (cell type: %s)" % (self.name, self.cell_type)

    def size(self):
        return 1

    def get_neuron_positions(self):
        return [(0, 0, 0)]


class PopulationTemplate(Population):
    def __init__(self,  name, n_neurons, cell_type):
        Population.__init__(self, name, cell_type)
        self.n_neurons = n_neurons
        self.neuron_positions = lambda i: (0, 0)

    def size(self):
        return self.n_neurons

    def __repr__(self):
        return "%s (cell type: %s, Template)" % (self.name, self.cell_type)

    def get_neuron_positions(self):
        return self.neuron_positions


class PopulationTemplateRandom(PopulationTemplate):
    def __init__(self, name, n_neurons, bounds, cell_type):
        """

        :param n_neurons: Number of neurons in this template
        :type n_neurons: int
        :param bounds: Bounds of the neuron collection template in 3D space
        :type bounds: RectangularBounds|SphericalBounds
        """
        PopulationTemplate.__init__(self, name, n_neurons, cell_type)
        self.bounds = bounds
        self.neuron_positions = csa.random2d(n_neurons, bounds.w, bounds.h)

    def size(self):
        return self.n_neurons


class PopulationTemplateGrid(PopulationTemplate):
    pass


class PopulationInstances(Population):
    def __init__(self, name, neuron_instances, cell_type):
        """

        :param neuron_instances: List of neuron instances
        :type neuron_instances: list[Neuron]
        """
        Population.__init__(self, name, cell_type)
        self.neuron_instances = neuron_instances

    def size(self):
        return len(self.neuron_instances)

    def __repr__(self):
        return "%s (cell type: %s, %d neuron instances)" % \
               (self.name, self.cell_type, len(self.neuron_instances))


class Neuron:
    def __init__(self, neuron_id, location=None):
        """

        :param neuron_id: Numerical identifier of the neuron. Must be unique inside a population
        :type neuron_id: int
        :param location: Position of the neuron in 3D space
        :type location: tuple[float]
        """
        self.neuron_id = neuron_id
        self.location = location or (0, 0, 0)


class SphericalBounds:
    def __init__(self, x, y, z, diameter):
        """

        :param x: x-coordinate of sphere center
        :type x: float
        :param y: y-coordinate of sphere center
        :type y: float
        :param z: z-coordinate of sphere center
        :type z: float
        :param diameter: Diameter of the sphere
        :type diameter: float
        """
        self.x = x
        self.y = y
        self.z = z
        self.d = diameter


class RectangularBounds:
    def __init__(self, x, y, z, w, h, d):
        """

        :param x: x-coordinate of the corner with the lowest x value
        :param y: y-coordinate of the corner with the lowest y value
        :param z: z-coordinate of the corner with the lowest z value
        :param w: Width of the box (x size)
        :param h: Height of the box (y size)
        :param d: Depth of the box (z size)
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
