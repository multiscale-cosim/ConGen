from _misc import neuroml_namespace as neuroNS
from projections import *
from populations import *
from inputs import *
from outputs import *
from model import *
from synapses import *
from distributions import *
from _misc import NetworkMLParsingError
import logging

logging.basicConfig(filename='/home/sandra/Documents/ViCoGen/ConGen/python/test.log', encoding='utf-8', level=logging.DEBUG)
    
def parse_model(model_xml):
    """

    :param model_xml: The xml element containing the whole model
    :type model_xml: xml.etree.ElementTree.Element
    :return: The parsed network model data structure
    :rtype: NetworkModel
    """
    populations_xml = model_xml.find("net:populations", neuroNS)
    projections_xml = model_xml.find("net:projections", neuroNS)
    inputs_xml = model_xml.find("nml:inputs", neuroNS)
    
    outputs_xml = model_xml.find("nml:outputs", neuroNS)

    populations = []
    if populations_xml is not None:
        for population_xml in populations_xml.getchildren():
            pop = parse_population(population_xml)
            populations.append(pop)

    projections = []
    if projections_xml is not None:
        for projection_xml in projections_xml.getchildren():
            proj = parse_projection(projection_xml)
            projections.append(proj)

    inputs = []
    if inputs_xml is not None:
        for input_xml in inputs_xml.getchildren():
            input_ = parse_input(input_xml)
            inputs.append(input_)

    outputs = []
    if outputs_xml is not None:
        for output_xml in outputs_xml.getchildren():
            output_ = parse_output(output_xml)
            outputs.append(output_)

    return NetworkModel(populations, projections, inputs, outputs)

def parse_model_multiscale(model_xml, labels):
    """
    :param model_xml: The xml element containing the whole model
    :type model_xml: xml.etree.ElementTree.Element
    :return: The parsed network model data structures for multiscale
    :rtype: dictionary with NetworkModel objects
    """
    models = {}

    populations_xml = model_xml.find("net:populations", neuroNS)
    projections_xml = model_xml.find("net:projections", neuroNS)
    inputs_xml = model_xml.find("net:inputs", neuroNS)
    outputs_xml = model_xml.find("nml:outputs", neuroNS)
    print("Populations", populations_xml)
    print("Projections", projections_xml)
    print("Inputs", inputs_xml)
    print("Outputs", outputs_xml)

    for key, val in labels.items():
        populations = []
        if populations_xml is not None:
            for population_xml in populations_xml.getchildren():
                pop = parse_population(population_xml, val)
                if pop:
                    populations.append(pop)

        projections = []
        if projections_xml is not None:
            for projection_xml in projections_xml.getchildren():
                proj = parse_projection(projection_xml, val)
                if proj:
                    projections.append(proj)

        inputs = []
        if inputs_xml is not None:
            for input_xml in inputs_xml.getchildren():
                input_ = parse_input(input_xml)
                inputs.append(input_)

        outputs = []
        if outputs_xml is not None:
            for output_xml in outputs_xml.getchildren():
                output_ = parse_output(output_xml)
                outputs.append(output_)
        models[key] = NetworkModel(populations, projections, inputs, outputs)

    return models

# --- Projection parsing ---
def parse_projection(projection_xml, label=""):
    """
    Parses Element with XML tag 'projection'

    :type projection_xml: xml.etree.ElementTree.Element
    :rtype: Projection
    """
    name = projection_xml.attrib["name"]
    source_name = projection_xml.attrib["source"]
    target_name = projection_xml.attrib["target"]
    if not label in source_name or label in target_name:
        return

    # Get synapse properties
    synprops_xml = projection_xml.find("net:synapse_props", neuroNS)

    synprops = parse_synapse_properties(synprops_xml)

    # Parse connectivity pattern or instances
    conn_pattern_xml = projection_xml.find("net:connectivity_pattern", neuroNS)
    conn_instances_xml = projection_xml.find("net:connections", neuroNS)
    if conn_pattern_xml is not None:
        return parse_connectivity_pattern(conn_pattern_xml, name, source_name, target_name, synprops)
    elif conn_instances_xml is not None:
        connections = []
        for conn_instance_xml in conn_instances_xml.findall("net:connection", neuroNS):
            connections.append(parse_connection_instance(conn_instance_xml))
        return InstancedConnections(name, source_name, target_name, synprops, connections)
    else:
        return Projection(name, source_name, target_name, synprops=synprops)


def parse_connection_instance(connection_xml):
    """
    Parses Element with XML tag 'connection'
    :type connection_xml: xml.etree.ElementTree.Element
    :rtype: ConnectionInstance
    """

    con_id = connection_xml.attrib['id']
    pre_cell_id = connection_xml.get("pre_cell_id", None)
    pre_segment_id = connection_xml.get("pre_segment_id", 0)
    pre_fraction_along = float(connection_xml.get("pre_fraction_along", 0.5))
    post_cell_id = connection_xml.get("post_cell_id", None)
    post_segment_id = connection_xml.get("post_segment_id", 0)
    post_fraction_along = float(connection_xml.get("post_fraction_along", 0.5))

    return ConnectionInstance(con_id, pre_cell_id, post_cell_id, pre_segment_id, post_segment_id,
                              pre_fraction_along, post_fraction_along)


def parse_connectivity_pattern(connection_xml, name, source_name, target_name, synprops):
    """
    Parses Element with XML tag 'connectivity_pattern'
    :type connection_xml: xml.etree.ElementTree.Element
    :rtype: ConnectivityPattern
    """

    # all_to_all
    pattern = connection_xml.find("net:all_to_all", neuroNS)
    if pattern is not None:
        return AllToAll(name, source_name, target_name, synprops)

    # fixed_probability
    pattern = connection_xml.find("net:fixed_probability", neuroNS)
    if pattern is not None:
        p = float(pattern.get("probability", 0.0))
        return FixedProbability(p, name, source_name, target_name, synprops)

    # one_to_one
    pattern = connection_xml.find("cg:one_to_one", neuroNS)  # Not actually in NeuroML
    print("One to One:",pattern)
    if pattern is not None:
        return OneToOne(name, source_name, target_name, synprops)

    # atlas_based
    pattern = connection_xml.find("cg:atlas_based", neuroNS)  # Not actually in NeuroML
    print("Atlas:",pattern)
    if pattern is not None:
        return AtlasBased(name, source_name, target_name, synprops)


    # per_cell
    pattern = connection_xml.find("net:per_cell_connection", neuroNS)
    if pattern is not None:
        direction = pattern.attrib.get("direction") == "PostToPre"
        nSource = int(pattern.attrib['num_per_source'])
        if 'max_per_target' in pattern.attrib:
            nMaxTarget = pattern.attrib['max_per_target']  # TODO: max target is not supported in CSA
        return PerCell(nSource, name, source_name, target_name, synprops, reverse=direction)

    # gaussian
    pattern = connection_xml.find("net:gaussian_connectivity_2d", neuroNS)
    if pattern is not None:
        sigma = float(pattern.attrib['sigma'])
        cutoff = float(pattern.attrib.get('cutoff', 100))
        return GaussianSpatialConnectivity(sigma, cutoff, name, source_name, target_name, synprops)

    raise NetworkMLParsingError(connection_xml, "Unknown connectivity pattern")


# --- Synapse Parsing ---

def parse_synapse_properties(synapse_props_xml):
    """
    Parses Element with XML tag 'synapse_props'
    :type synapse_props_xml: xml.etree.ElementTree.Element
    :rtype: SynapseProperties
    """
    synapse_type = synapse_props_xml.attrib['synapse_type']

    # Check if we have a distribution for weight
    weight_xml = synapse_props_xml.find("net:weight", neuroNS)
    if weight_xml is not None:
        weight = parse_distributed_value(weight_xml)
    elif 'weight' in synapse_props_xml.attrib:
        weight = synapse_props_xml.attrib['weight']
    else:
        weight = Projection._default_weight

    # Check if we have a distribution for delay
    internal_delay_xml = synapse_props_xml.find("net:internal_delay", neuroNS)
    if internal_delay_xml is not None:
        internal_delay = parse_distributed_value(internal_delay_xml)
    elif 'internal_delay' in synapse_props_xml.attrib:
        internal_delay = synapse_props_xml.attrib['internal_delay']
    else:
        internal_delay = Projection._default_delay

    return SynapseProperties(weight, internal_delay, SynapseModel(synapse_type))


def parse_distributed_value(value_xml):
    """
    Parses Element that contains either a single float value or a distribution
    :type value_xml: xml.etree.ElementTree.Element
    :rtype: float|Distribution
    """

    try:
        value = float(value_xml.text)
        return value
    except ValueError:
        return parse_distribution(value_xml[0])


def parse_distribution(distribution_xml):
    """
    Parses a distribution Element. So far the tags GaussianDistribution and UniformDistribution are supported.
    :type distribution_xml: xml.etree.ElementTree.Element
    :rtype: Distribution
    """
    if distribution_xml.tag == '{%s}GaussianDistribution' % neuroNS['net']:
        center = distribution_xml.attrib['center']
        deviation = distribution_xml.attrib['deviation']
        return GaussianDistribution(center, deviation)

    elif distribution_xml.tag == '{%s}UniformDistribution' % neuroNS['net']:
        upper = distribution_xml.attrib['upper']
        lower = distribution_xml.attrib['lower']
        return UniformDistribution(lower, upper)

    else:
        raise NetworkMLParsingError(distribution_xml, "Unknown Distribution")


# --- Population Parsing ---

def parse_population(population_xml, tag=''):
    """
    Parses Element with XML tag 'population'

    :type population_xml: xml.etree.ElementTree.Element
    :rtype: Population"""
    name = population_xml.attrib['name']

    if not tag in name:
        return
    cell_type = population_xml.attrib['cell_type']
    instances_xml = population_xml.find('net:instances', neuroNS)
    template_xml = population_xml.find('net:pop_location', neuroNS)
    if instances_xml is not None:
        instances = parse_population_instance(instances_xml)
        population = PopulationInstances(name, instances, cell_type)
    elif template_xml is not None:
        population = parse_population_template(template_xml, name, cell_type)
    else:
        population = Population(name, cell_type)

    return population


def parse_population_instance(population_instance_xml):
    """
    Parses Element with XML tag 'instances'

    :type population_instance_xml: xml.etree.Element
    :rtype: list[Neuron]"""
    neuron_instances = []
    for neuron_instance_xml in population_instance_xml.findall('net:instance', neuroNS):
        neuron_id = neuron_instance_xml.attrib['id']
        location_xml = neuron_instance_xml.find('net:location', neuroNS)
        if location_xml is not None:
            location = (float(location_xml.attrib['x']),
                        float(location_xml.attrib['y']),
                        float(location_xml.attrib['z']))
        else:
            location = (0, 0, 0)
        neuron = Neuron(neuron_id, location)
        neuron_instances.append(neuron)
    return neuron_instances


def parse_population_template(population_template_xml, name, cell_type):
    """
    Parses Element with XML tag 'pop_location'

    :type population_template_xml: xml.etree.ElementTree.Element
    :rtype: PopulationTemplate"""
    random_template = population_template_xml.find("net:random_arrangement", neuroNS)
    grid_template = population_template_xml.find("net:grid_template", neuroNS)

    if random_template is not None:
        n = int(random_template.attrib['population_size'])
        loc_xml = random_template.find('net:spherical_location', neuroNS) or random_template.find('net:rectangular_location', neuroNS)
        if loc_xml is None:
            raise NetworkMLParsingError(random_template)
        if loc_xml.tag == 'spherical_location':
            loc = parse_spherical_bounds(loc_xml)
        else:
            loc = parse_rectangular_bounds(loc_xml)
        return PopulationTemplateRandom(name, n, loc, cell_type)
    elif grid_template is not None:
        return PopulationTemplateGrid(name, 0, cell_type)


def parse_spherical_bounds(spherical_bounds_xml):
    """
    Parses Element with XML tag 'spherical_location'
    :param spherical_bounds_xml:
    :type spherical_bounds_xml: xml.etree.ElementTree.Element
    :return:
    :rtype: SphericalBounds
    """
    center = spherical_bounds_xml.find('net:center', neuroNS)
    if center is None:
        raise NetworkMLParsingError(spherical_bounds_xml)
    x = float(center.attrib['x'])
    y = float(center.attrib['y'])
    z = float(center.attrib['z'])
    diameter = center.attrib['diameter']
    return SphericalBounds(x, y, z, diameter)


def parse_rectangular_bounds(rectangular_bounds_xml):
    """
    Parses Element with XML tag 'rectangular_location'
    :param rectangular_bounds_xml:
    :type rectangular_bounds_xml: xml.etree.ElementTree.Element
    :return:
    :rtype: RectangularBounds
    """
    corner = rectangular_bounds_xml.find('net:corner', neuroNS)
    size = rectangular_bounds_xml.find('net:size', neuroNS)
    if corner is None or size is None:
        raise NetworkMLParsingError(rectangular_bounds_xml)
    x = float(corner.attrib['x'])
    y = float(corner.attrib['y'])
    z = float(corner.attrib['z'])
    w = float(size.attrib['width'])
    h = float(size.attrib['height'])
    d = float(size.attrib['depth'])
    return RectangularBounds(x, y, z, w, h, d)

# --- Parsing Inputs ---


def parse_input(input_xml):
    """
    Parses Element with XML tag 'input'
    :param input_xml:
    :type input_xml: xml.etree.ElementTree.Element
    :return: Parsed input
    :rtype: Input
    """

    name = input_xml.attrib['name']
    poisson_input_xml = input_xml.find("nml:random_stim", neuroNS)
    if poisson_input_xml is not None:
        frequency = float(poisson_input_xml.attrib['frequency'])
        return PoissonInput(name, frequency)
    if "spike_to_rate" in name:
        return SpikeToRate(name)
    if "rate_to_spike" in name:
        return RateToSpike(name)
    

    raise NetworkMLParsingError(input_xml, "Unsupported Input Type")

def parse_output(output_xml):
    """
    Parses Element with XML tag 'output'
    :param output_xml:
    :type output_xml: xml.etree.ElementTree.Element
    :return: Parsed output
    :rtype: Output
    """

    name = output_xml.attrib['name']

    output_m_xml = output_xml.find("nml:monitor", neuroNS)
    if output_m_xml is not None:
        return Monitor(name)

    raise NetworkMLParsingError(output_xml, "Unsupported Output Type")
