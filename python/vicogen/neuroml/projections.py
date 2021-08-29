import csa
import numpy
import logging
import synapses
from distributions import Distribution

try:
    raise ImportError  # Disabled for now
    import libcsa
    csa.random = libcsa.random
    csa.oneToOne = libcsa.oneToOne
    csa.full = libcsa.allToAll
except ImportError:
    logging.info("Running without libcsa, using python csa as fallback")


class Projection:

    _default_weight = 1.0
    _default_threshold = 0.0
    _default_delay = 0.0
    _default_synapse_type = "default"

    def __init__(self, name, source, target, synprops):
        """

        :param name: Identifier of this projection
        :param source: Source population. This can be either given as a Population object or
            as the string identifier of the Population
        :type  source: Population|str
        :param target: Target population. This can be either given as a Population object or
            as the string identifier of the Population
        :type  target: Population|str
        :param synprops: The properties of the synapses
        :type synprops: synapses.SynapseProperties

        """
        self.name = name

        if type(source) is str:
            self.source_identifier = source
            self.source = None
        else:
            self.source = source
            self.source_identifier = source.name

        if type(target) is str:
            self.target_identifier = target
            self.target = None
        else:
            self.target = target
            self.target_identifier = target.name

        self.synapse_properties = synprops

    def __repr__(self):
        return "%s (synapse type: %s)" % (self.name, self.synapse_properties.synapse_model)

    def cset(self):
        weight = self.synapse_properties.weight
        if isinstance(weight, Distribution):
            weight = weight.vset()

        delay = self.synapse_properties.delay
        if isinstance(delay, Distribution):
            delay = delay.vset()

        mask = self.mask() * csa.elementary.cross(xrange(self.source.size()),
                                                            xrange(self.target.size()))
        cs = csa.cset(mask, weight, delay)

        return cs

    def mask(self):
        return csa.empty


class InstancedConnections(Projection):
    def __init__(self, name, source, target, synprops, connections):
        Projection.__init__(self, name, source, target, synprops)
        self.connections = connections

    def __repr__(self):
        return "%s (synapse type: %s, %d connection instances)" % \
               (self.name, self.synapse_properties.synapse_model, len(self.connections))


class ConnectionInstance:
    def __init__(self, con_id, pre_cell_id=None, post_cell_id=None, pre_segment_id=0, post_segment_id=0,
                 pre_fraction_along=0.5, post_fraction_along=0.5):
        self.con_id = con_id
        self.pre_cell_id = pre_cell_id
        self.post_cell_id = post_cell_id
        self.pre_segment_id = pre_segment_id
        self.post_segment_id = post_segment_id
        self.pre_fraction_along = pre_fraction_along
        self.post_fraction_along = post_fraction_along


class ConnectivityPattern(Projection):
    """
    :var self.mask: The csa mask that represents this connectivity pattern
    :type self.mask: csa.Mask
    """
    def __init__(self, name, source, target, synprops):
        Projection.__init__(self, name, source, target, synprops)
        self._mask = csa.empty

    def __repr__(self):
        return "%s (synapse type: %s, Template)" % (self.name, self.synapse_properties.synapse_model)

    def mask(self):
        return self._mask


class AllToAll(ConnectivityPattern):
    def __init__(self, name, source, target, synprops):
        ConnectivityPattern.__init__(self, name, source, target, synprops)
        self._mask = csa.full


class OneToOne(ConnectivityPattern):  # Not actually in NeuroML
    def __init__(self, name, source, target, synprops):
        ConnectivityPattern.__init__(self, name, source, target, synprops)
        self._mask = csa.oneToOne

class AtlasBased(ConnectivityPattern):
    def __init__(self, name, source, target, synprops):
        ConnectivityPattern.__init__(self, name, source, target, synprops)
        self._mask = synprops['Connectivity Matrix']


class FixedProbability(ConnectivityPattern):
    def __init__(self, probability, name, source, target, synprops):
        """

        :param probability: Probability with which a connection between a source and target neuron is created
         :type probability: float
        """
        ConnectivityPattern.__init__(self, name, source, target, synprops)
        self.probability = probability
        self._mask = csa.random(probability)


class PerCell(ConnectivityPattern):
    def __init__(self, n_source, name, source, target, synprops, reverse=False):
        """
        Connects a fixed number of target neurons to a source neuron
        :param n_source: number of target neurons connected to a single source neuron
        :type n_source: int
        :param reverse: Instead of a fixed number of target neurons for each source neuron,
            a fixed number of source neurons is connected to a target neuron.
        :type reverse: bool
        """
        ConnectivityPattern.__init__(self, name, source, target, synprops)
        if reverse:
            self._mask = csa._elementary.FanInRandomOperator(n_source)
        else:
            self._mask = csa._elementary.FanOutRandomOperator(n_source)


class GaussianSpatialConnectivity(ConnectivityPattern):
    def __init__(self, sigma, cutoff, name, source, target, synprops):
        """
        Defines a gaussian connectivity model based on the spatial positions of the neurons.
        Neurons closer to each other on their mapped planes connect with higher probability.
        :param sigma: The size of the gaussian model. Higher values result in more connections.
        :param cutoff: The cutoff value for the gaussian connections. Neurons with a distance greater than the cutoff
            value will not be connected
        :type sigma: float
        :type cutoff: float
        """
        ConnectivityPattern.__init__(self, name, source, target, synprops)
        self._mask = csa.gaussian(sigma, cutoff)

    def mask(self):
        pos_src = self.source.neuron_positions
        pos_tar = self.target.neuron_positions
        distance = csa.euclidMetric2d(pos_src, pos_tar)
        return csa.random * (self._mask * distance)


def csa_to_matrix(cset, src_n=30, tar_n=30):
    """
    Returns an array of connections for a connection set
    :param cset: The connection set
    :type cset: csa.ConnectionSet
    :param src_n: Number of neurons in the source population
    :type src_n: int
    :param tar_n: Number of neurons in the target population
    :type tar_n: int
    :return: A numpy array of the connection matrix
    :rtype: numpy.ndarray
    """
    a = numpy.zeros((src_n, tar_n))
    for connection in csa.elementary.cross(range(src_n), range(tar_n)) * cset:
        a[connection[0], connection[1]] += 1.0
    return a


def csa_to_iterator(cset, src_n, tar_n):
    """
    Returns an iterator of connections for a connection set
    :param cset: The connection set
    :type cset: csa.ConnectionSet
    :param src_n: Number of neurons in the source population
    :type src_n: int
    :param tar_n: Number of neurons in the target population
    :type tar_n: int
    :return: A list of connection indices
    :rtype: collections.Iterable[(int, int)]
    """
    for conn in csa.elementary.cross(range(src_n), range(tar_n)) * cset:
        yield conn

