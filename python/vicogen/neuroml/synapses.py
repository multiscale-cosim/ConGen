from distributions import Distribution


class SynapseProperties:
    def __init__(self, weight, delay, synapse_model):
        """

        :param weight: The synaptic strength of a connection. Can be given as float or as a distribution
        :type weight: float|Distribution
        :param delay:
        :type delay: float|Distribution
        :param synapse_model: The synapse model to use. For now this is a NEST model.
        :type synapse_model: SynapseModel
        """
        self.weight = weight
        self.delay = delay
        self.synapse_model = synapse_model


class SynapseModel:
    def __init__(self, nest_identifier):
        self.nest_identifier = nest_identifier
