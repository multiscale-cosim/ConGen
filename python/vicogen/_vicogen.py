from __future__ import print_function
import sys

import logging

import neuroml #from .
import json


def parse_model(filename):
    """
    Parse a NeuroML file

    :param filename: The name of the NeuroML file to parse
    :type filename: str
    :return: The parsed network model
    :rtype: neuroml.NetworkModel
    """
    with open(filename, 'r') as f:
        return neuroml.read_xml(f)


def parse_model_multiscale(filename, tags=["NEST_","TVB_"]):
    """
    Parse a NeuroML file for multiscale simulation

    :param filename: The name of the NeuroML file to parse
    :type filename: str
    :param tags: Tags used to split the hierarchies in model
    :type tags: str array
    :return: The parsed network model
    :rtype: neuroml.NetworkModel
    """
    with open(filename, 'r') as f:
        return neuroml.read_xml_multiscale(f, tags)


def print_connections(model, out=sys.stdout):
    """
    Print all the connections fo a model

    :param model: The model to print
    :type model: neuroml.NetworkModel
    :param out: The output stream to write to
    :type out: IO
    """
    for proj in model.projections:
        connections = neuroml.get_connections(proj)
        print("Connections for " + str(proj.name))
        for conn in connections:
            print(conn, file=out)


def build_nest_model(model, options=None):
    """
    Build a model in NEST

    :param model:
    :type model: neuroml.NetworkModel
    :return: The built model in NEST
    """
    from . import _nest

    return _nest.nest_build_model(model, options)

def build_tvb_model(model, options=None):
    """
    Build the multiscale TVB model

    :param model:
    :type model: neuroml.NetworkModel
    :return: The built model in TVB
    """
    from . import _tvb

    return _tvb.tvb_build_model(model, options)

def build_nest_multiscale_file(model, options=None):
    """
    Build a multiscale file in NEST

    :param model:
    :type model: neuroml.NetworkModel
    :return:
    """
    from . import _nest

    return _nest.nest_build_multiscale_file(model, options)

def build_tvb_multiscale_file(tvb_model, tvb_label, options=None):
    """
    Build the multiscale TVB file

    :param model:
    :type model: neuroml.NetworkModel
    :return: 
    """
    from . import _tvb

    return _tvb.tvb_build_model(tvb_model, tvb_label, options)

def build_translator_multiscale_file(model, options=None):
    """
    Build a translator files

    :param model:
    :type model: neuroml.NetworkModel
    :return: 
    """
    from . import _translator

    _translator.build_translator_file(model, options)

def simulate_nest_model(model, sim_time=100.0, options=None):
    """
    Simulates a built NEST model. Calls build_nest_model() first if model is a NetworkModel object.
    :param model: The model to simulate
    :type model: _nest.NestModel|neuroml.NetworkModel
    :return:
    """
    from . import _nest

    if isinstance(model, _nest.NestModel):
        nest_model = model
    else:
        nest_model = build_nest_model(model, options)

    _nest.nest_simulate_model(nest_model, {'sim_time': sim_time})


def simulate_tvb_model(model, sim_time=100.0, options=None):
    """
    Simulates a built TVB model. Calls build_tvb_model() first if model is a NetworkModel object.
    :param model: The model to simulate
    :type model: _tvb.TVBModel|neuroml.NetworkModel
    :return:
    """
    from . import _tvb

    if isinstance(model, _tvb.TVBModel):
        tvb_model = model
    else:
        tvb_model = build_tvb_model(model, options)

    _tvb.tvb_simulate_model(tvb_model, {'sim_time': sim_time})

def multiscale(model, labels, sim_time=100.0, options=None):
    """
    Simulates a multiscale model. Calls build_nest_model(), build_translator_model(), build_tvb_model() with the NetworkModel object.
    :param models: The models at each scale
    :type model:neuroml.NetworkModel
    :return:
    """
    from . import _tvb
    from . import _nest
    

    nest_model = build_nest_model(model["NEST"], options)
    build_nest_multiscale_file(nest_model, options)
    build_tvb_multiscale_file(model["TVB"], labels["TVB"], options)
    build_translator_multiscale_file(nest_model)    

def handle_arguments(args):
    logging.basicConfig(level=args.loglevel)
    
    if args.multiscale:
        labels = json.loads(args.multiscale_labels)
        models = neuroml.read_xml_multiscale(args.modelfile, labels)
        multiscale(models, labels, args.simulate, {})
    else :
        model = neuroml.read_xml(args.modelfile)
        if args.write_connections:
            # If -c or --write-connections is active, only print connectivity and return
            print_connections(model, args.outfile)
            return
        elif args.simulate:
            if  args.nest:
                simulate_nest_model(model, args.simulate, {})
            elif  args.tvb:
                simulate_tvb_model(model, args.simulate, {})
