from __future__ import print_function
import sys

import logging

import neuroml #from .


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
    Build a model in TVB

    :param model:
    :type model: neuroml.NetworkModel
    :return: The built model in TVB
    """
    from . import _tvb

    return _tvb.tvb_build_model(model, options)

def build_translator(model, options=None):
    """
    Build a translator

    :param model:
    :type model: neuroml.NetworkModel
    :return: The built translator model
    """
    from . import _translator

    return _translator.translator_build_model(model, options)


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

    if isinstance(model, _tvb.NestModel):
        tvb_model = model
    else:
        tvb_model = build_tvb_model(model, options)

    _tvb.tvb_simulate_model(tvb_model, {'sim_time': sim_time})

def simulate_multiscale(model, sim_time=100.0, options=None):
    """
    Simulates a multiscale model. Calls build_nest_model(), build_translator_model(), build_tvb_model() with the NetworkModel object.
    :param model: The model to simulate
    :type model:neuroml.NetworkModel
    :return:
    """
    from . import _tvb
    from . import _nest
    from . import _tvb_to_nest
    from . import _nest_to_tvb


    tvb_model = build_tvb_model(model, options)

    _tvb.tvb_simulate_model(tvb_model, {'sim_time': sim_time})

def handle_arguments(args):
    logging.basicConfig(level=args.loglevel)

    model = neuroml.read_xml(args.modelfile)
    print(args.simulate)
    if args.write_connections:
        # If -c or --write-connections is active, only print connectivity and return
        print_connections(model, args.outfile)
        return
    elif args.simulate:
        if args.multiscale:
            simulate_multiscale(model, args.simulate, {})

        elif args.nest:
            simulate_nest_model(model, args.simulate, {})
 
        elif args.tvb:
            simulate_tvb_model(model, args.simulate, {})

