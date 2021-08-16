import unittest
import random
import numpy as np
import sys
sys.argv.append("--verbosity=QUIET")  # This seems to shut up nest a bit

import nest
import nest.raster_plot

import vicogen
import vicogen.neuroml as nml


class NestSimulationTest(unittest.TestCase):
    def setUp(self):
        pass

    def testNestSimulationAllToAll(self):
        model = vicogen.parse_model("models/all_to_all_model.xml")
        nestModel = vicogen.build_nest_model(model)

        vicogen._nest.nest_seed(42)

        # Create a spike detector to measure the spiking activity
        sd = nest.Create('spike_detector')
        nest.Connect(nestModel.populations['PopB'], sd)

        vicogen.simulate_nest_model(nestModel)

        events = nest.GetStatus(sd, 'events')[0]

        eventsControl = {u'senders': np.array([76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,
                                               89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101,
                                               102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
                                               115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 76, 77,
                                               78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                                               91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,
                                               104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
                                               117, 118, 119, 120, 121, 122, 123, 124, 125, 76, 77, 78, 79,
                                               80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
                                               93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105,
                                               106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
                                               119, 120, 121, 122, 123, 124, 125, 76, 77, 78, 79, 80, 81,
                                               82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94,
                                               95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
                                               108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                                               121, 122, 123, 124, 125]),
                         u'times': np.array([44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3,
                                             44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3,
                                             44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3,
                                             44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3,
                                             44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3, 44.3,
                                             44.3, 44.3, 44.3, 44.3, 44.3, 54.4, 54.4, 54.4, 54.4,
                                             54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4,
                                             54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4,
                                             54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4,
                                             54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4,
                                             54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4, 54.4,
                                             54.4, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9,
                                             71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9,
                                             71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9,
                                             71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9,
                                             71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 71.9,
                                             71.9, 71.9, 71.9, 71.9, 71.9, 71.9, 94.3, 94.3, 94.3,
                                             94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3,
                                             94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3,
                                             94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3,
                                             94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3,
                                             94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3, 94.3,
                                             94.3, 94.3])}

        np.testing.assert_array_equal(events['senders'], eventsControl['senders'])
        np.testing.assert_allclose(events['times'], eventsControl['times'], atol=0.01)

    def testNestSpatialConnectivity(self):
        model = vicogen.parse_model("models/spatial_connectivity_model.xml")
        nestModel = vicogen.build_nest_model(model)

        vicogen._nest.nest_seed(42)

        # Create a spike detector to measure the spiking activity
        sd = nest.Create('spike_detector')
        nest.Connect(nestModel.populations['PopB'], sd)

        vicogen.simulate_nest_model(nestModel)

        events = nest.GetStatus(sd, 'events')[0]

        eventsControl = {u'senders': np.array([86, 76, 124, 112, 95, 102, 105, 84, 79, 93, 100, 117, 101,
                                               114, 98, 113, 106, 89, 94, 121, 103, 107, 118, 92, 123, 78,
                                               88, 111, 82, 125, 120, 96, 81, 102, 76, 124, 86, 105, 119,
                                               113, 104, 108, 94, 89, 107, 93, 115, 121, 80, 116, 95, 98,
                                               117, 90, 84, 87, 79, 92, 78, 77, 106, 83, 96, 114, 118,
                                               103, 123, 86, 76, 125]),
                         u'times': np.array([44.9, 45.3, 45.6, 46.4, 46.5, 46.7, 47.1, 47.3, 47.9,
                                             48.4, 48.6, 48.8, 49.4, 49.9, 50.2, 50.5, 52.4, 53.,
                                             53., 53.1, 53.7, 53.7, 53.8, 53.9, 54., 54.1, 54.1,
                                             54.1, 54.3, 54.3, 55., 55.3, 56.4, 71.4, 72.1, 72.9,
                                             73.5, 73.5, 73.6, 73.7, 73.8, 73.8, 74.2, 74.3, 74.3,
                                             74.5, 74.5, 74.5, 74.7, 74.7, 74.8, 75., 75., 75.3,
                                             75.4, 75.4, 75.5, 75.5, 75.6, 75.7, 76.2, 76.3, 76.6,
                                             76.9, 77.5, 77.8, 98.8, 99., 99.3, 99.4])}

        np.testing.assert_array_equal(events['senders'], eventsControl['senders'])
        np.testing.assert_allclose(events['times'], eventsControl['times'], atol=0.01)