import nest
import numpy

from . import neuroml
import logging


class NestModel:
    def __init__(self):
        self.populations = {}
        self.inputs = {}


def nest_build_model(network_model, options=None):
    """
    Builds a model in nest and saves the population and input indices in a NestModel object
    :param network_model: The network model to build in nest
    :type network_model: neuroml.NetworkModel
    :return: The model built in nest
    :rtype: NestModel
    """
    nest.ResetKernel()
    if options:
        nest.SetKernelStatus(options)  # TODO: Check options before passing to nest

    nest_model = NestModel()
    logging.info("Building NEST Populations")
    for population in network_model.populations:
        nest_model.populations[population.name] = nest_build_population(population)

    logging.info("Building NEST Input Generators")
    for input_ in network_model.inputs:
        nest_model.inputs[input_.name] = nest_build_input(input_)

    logging.info("Connecting NEST Populations")
    for projection in network_model.projections:
        nest_build_projection(projection, nest_model)

    logging.info("Finished building network")

    return nest_model


def nest_build_projection(projection, nest_model):
    """
    Connects nest populations from a Projection object
    :param projection: The projection with a source and target name identifier
    :type projection: neuroml.projections.Projection
    :param nest_model: The nest model with the ids of the generated connections
    :type nest_model: NestModel
    """
    source_ids = nest_model.populations.get(projection.source_identifier) or nest_model.inputs.get(projection.source_identifier)
    target_ids = nest_model.populations[projection.target_identifier]
    cset = projection.cset()  # TODO: handle other connections
    nest.CGConnect(source_ids, target_ids, cset,
                   {'weight': 0, 'delay': 1})  # Nest needs to know what the value sets mean, so we give it the indices of of our ValueSets


def nest_build_population(population):
    """
    Builds a NEST population from a Population object and returns the generated IDs
    :param population: The population to generate
    :type population: neuroml.populations.Population
    :return: A list of generated nest indices
    :rtype: list[int]
    """
    cell_type = population.cell_type

    n_neurons = population.size()
    return nest.Create(cell_type, n_neurons)


def nest_build_input(input):
    if isinstance(input, neuroml.inputs.PoissonInput):
        return nest.Create('poisson_generator', params={'rate': input.rate})


def nest_simulate_model(nest_model, options):
    logging.info("Starting NEST simulation")
    nest.Simulate(options['sim_time'])
    logging.info("Finished NEST simulation")


def nest_seed(seed):
    """Seed all of NESTs RNGs"""
    msd = seed
    N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
    # pyrngs = [numpy.random.RandomState(s) for s in range(msd, msd + N_vp)]
    nest.SetKernelStatus({'grng_seed': msd + N_vp})
