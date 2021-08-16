from populations import Population
from projections import Projection


class NetworkModel:
    """

    :param populations:
     :type populations: list[Population]
    :param projections:
     :type projections: list[Projection]
    :param inputs:
    """
    def __init__(self, populations, projections, inputs):
        """

        :param populations:
         :type populations: list[Population]
        :param projections:
         :type projections: list[Projection]
        :param inputs:
        """
        self.populations = populations
        self.projections = projections
        self.inputs = inputs

        self.populations_dict = {}
        self.inputs_dict = {}

        self.rebuild_populations_dict()
        self.rebuild_inputs_dict()

        self.update_references()

    def update_references(self, overwrite=False):
        for proj in self.projections:
            if proj.source is None or overwrite:
                proj.source = self.populations_dict.get(proj.source_identifier) or \
                              self.inputs_dict.get(proj.source_identifier)
            if proj.target is None or overwrite:
                proj.target = self.populations_dict.get(proj.target_identifier)

    def rebuild_populations_dict(self):
        self.populations_dict = dict((pop.name, pop) for pop in self.populations)

    def rebuild_inputs_dict(self):
        self.inputs_dict = dict((input_.name, input_) for input_ in self.inputs)

