import argparse
import sys

import logging


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('modelfile', type=argparse.FileType('r'),
                        help="The NeuroML compatible XML file that describes the model")
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), nargs="?", default=sys.stdout,
                        help="File to write output to")
    parser.add_argument('-t', '--simulate', type=float, default=0, metavar="SIMTIME",
                        help="Simulate the model for a given amount of milliseconds")
    parser.add_argument('-n', '--nest', type=bool, default=False, metavar="use_nest",
                        help="Use Nest")
    parser.add_argument('-b', '--tvb', type=bool, default=False, metavar="use_tvb",
                        help="Use Nest")
    parser.add_argument('-m', '--multiscale', type=bool, default=False, metavar="use_multiscale",
                        help="Generate a multiscale simulation")
    parser.add_argument('-l', '--multiscale-labels', type=str, default='{"NEST":"l","TVB":"Brain_region_"}', metavar="multiscale_labels",
                        help="Define multiscale labels for model")
    parser.add_argument('-c', '--write-connections', action='store_true',
                        help="Instead of simulating the network, parse the connections and write them to output")
    parser.add_argument('--nest-options')

    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )

    args = parser.parse_args()
    return args
