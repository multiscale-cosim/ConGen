import neuroml
import logging
from tvb.simulator.lab import *
import numpy as np
import numpy.random as rgn
import math

from numpy import corrcoef


class TVBModel:
    """
    Builds a model in tvb and saves the population, output and inputs Model object
    :param network_model: The network model to build in tvb
    :type network_model: neuroml.NetworkModel
    :return: The model built in tvb
    :rtype: TVBModel
    """
    
    def __init__(self, sim_length, g, s, dt, period, omega = 60, filename='connectivity_68.zip'):
        self.populations = {}
       	self.inputs = {}
       	self.outputs = {}
	self.sim_length = sim_length
	self.g = np.array([g])
	self.s = np.array([s])
	self.dt = dt
	self.period = period
	self.omega = omega * 2.0 * math.pi / 1e3
	(self.connectivity, self.coupling) = self.tvb_connectivity(filename)
	self.SC = self.connectivity.weights
		

    def tvb_connectivity(self, filename):
	white_matter = connectivity.Connectivity.from_file(source_file=filename)
	white_matter.configure()
	white_matter.speed = np.array([self.s])
	white_matter_coupling = coupling.Linear(a=self.g)
	return white_matter, white_matter_coupling

    def tvb_build_input(self, inputs):
        self.id_proxy = inputs.id
        return

    def tvb_build_output(self, outputs):
        self.id_proxy = inputs.id
        return
	
    def tvb_python_model(self, modelExec):
	model = 'models.' + modelExec + '()'
	populations = eval(model)
	populations.configure()
	populations.omega = np.array([self.omega])
	return populations

   def tvb_simulate_model(self, modelExec):
	# Initialize Model
	model = self.tvb_python_model(modelExec)
	# Initialize integrator
	# integrator = integrators.EulerDeterministic(dt=self.dt)
	integrator = integrators.EulerStochastic(dt=0.1, noise=noise.Additive(nsig=np.array([1e-5])))
	# Initialize Monitors
	monitorsen = (monitors.TemporalAverage(period=self.period))
        # special monitor for MPI
        monitor_IO = Interface_co_simulation(
           id_proxy=self.id_proxy,
           time_synchronize=cosim['time_synchronize']
            )
        monitorsen.append(monitor_IO)
	# Initialize Simulator
	sim = simulator.Simulator(model=model, connectivity=self.connectivity,
							  coupling=coupling.Linear(a=np.array([0.5 / 50.0])), integrator=integrator,
								  monitors=[monitorsen])
	sim.configure()
	(time, data) = sim.run(simulation_length=self.sim_length)[0]

	return (time, data)


def tvb_build_model(network_model, options=None):
    tvb_model = TVBModel()
    logging.info("Building TVB Populations")
    for population in network_model.populations:
        nest_model.populations[population.name] = nest_build_population(population)

    logging.info("Linking to inputs")
    for input_ in network_model.inputs:
        tvb_model.tvb_build_input(input_)

    logging.info("Linking to outputs")
    for output_ in network_model.outputs:
        tvb_model.tvb_build_output(output_)

    logging.info("Connecting TVB Populations")
    for projection in network_model.projections:
        tvb_model.tvb_connectivity(projection, nest_model)

    logging.info("Finished building network")

    return tvb_model


def build_tvb_file(model, options)(network_model, options=None):


