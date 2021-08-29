from populations import *
from projections import *
from model import *
import parsing

import xml.etree.cElementTree as ET


def read_xml(xmlfile):
    """ Reads and parses an xml file and returns a data structure

    :param xmlfile: The xml file to parse
    :type xmlfile: file
    :return: The network model data structure
    :rtype: NetworkModel
    """
    et = ET.parse(xmlfile)
    root = et.getroot()
    return parsing.parse_model(root)

def read_xml_multiscale(xmlfile, labels):
    """ Reads and parses an xml file and returns a data structure
    which is useful for a multiscale simulation.

    :param xmlfile: The xml file to parse
    :type xmlfile: file
    :return: The network model data structure
    :rtype: NetworkModel
    """
    et = ET.parse(xmlfile)
    root = et.getroot()
    return parsing.parse_model_multiscale(root, labels)


def get_connections(projection):
    """
    Returns a list of connections for a projection generated with CSA
    :param projection:
    :type projection: Projection
    :return: A list of connection indices
    :rtype: collections.Iterable[(int, int)]
    """
    pop_size_source = projection.source.size() #projection.source.neurons.size()
    pop_size_target = projection.target.size()
    if isinstance(projection, ConnectivityPattern): #projection.connections
        return csa_to_iterator(projection.mask(), pop_size_source, pop_size_target)
    else:
        return [(x.source, x.target) for x in projection.connections] #projection.connections


def get_connectivity_matrix(projection):
    """
    Returns a connectivity matrix of the given projection
    :param projection:
    :type projection: Projection
    :return: A numpy array of the connection matrix
    :rtype: numpy.ndarray
    """
    # TODO: Single connections
    pop_size_source = projection.source.size()
    pop_size_target = projection.target.size()
    return csa_to_matrix(projection.cset(), pop_size_source, pop_size_target)

