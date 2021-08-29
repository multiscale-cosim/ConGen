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

    def tvb_build_proxy(self, inputs, tvb_label):
        self.id_proxy = inputs.name[inputs.name.find(tvb_label):]
        print(self.id_proxy, flush=True)
        return

    def tvb_python_model(self, modelExec):
        model = 'models.' + modelExec + '()'
        populations = eval(model)
        populations.configure()
        populations.omega = np.array([self.omega])
        return populations

    def tvb_simulate_model(self):
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
        sim = simulator.Simulator(model=self, connectivity=self.connectivity,
                        coupling=coupling.Linear(a=np.array([0.5 / 50.0])), integrator=integrator,
                        monitors=[monitorsen])
        sim.configure()
        (time, data) = sim.run(simulation_length=self.sim_length)[0]
        return (time, data)


def tvb_build_model(network_model, tvb_label, options=None):
    tvb_model = TVBModel(1000, 1, 1, 0.1, 10)
    logging.info("Building TVB Populations")
    modelbuilt = False
    for population in network_model.populations:
        if not modelbuilt:
            if population.cell_type == "nmm_kuramoto":
                tvb_model.tvb_python_model("Kuramoto")
            elif population.cell_type == "nmm_2doscillator":
                tvb_model.tvb_python_model("2DOscillator")
        if population.cell_type == "proxy":
            tvb_model.tvb_build_proxy(population, tvb_label) #Get the id

    logging.info("Connecting TVB Populations")
    for projection in network_model.projections:
        if "AtlasBased" in type(projection).__name__:
            print(type(projection).__name__, projection._mask) 
            tvb_model.tvb_connectivity(projection._mask)

    logging.info("Finished building network")
    return tvb_model


def build_tvb_file(tvb_model, options=None):
    from string import Template
    with open("./vicogen/_run_mpi_tvb_template.sh", 'r') as tempfile:
        with open("./vicogen/_run_mpi_tvb_ConGen.sh", 'w+') as outfile:
            t = Template(tempfile.read())
            sub = str(tvb_model.id_proxy[0])
            s = t.safe_substitute(id_p="{}".format(sub))
            outfile.write(s)


