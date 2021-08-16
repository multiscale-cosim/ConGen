import unittest
import random
import numpy as np

import vicogen
import vicogen.neuroml as nml


class ParsingTest(unittest.TestCase):
    def setUp(self):
        pass

    def testParseAllToAll(self):
        model = vicogen.parse_model("models/all_to_all_model.xml")

        # Assert number of populations and projections is correct
        self.assertEqual(len(model.populations), 2)
        self.assertEqual(len(model.inputs), 1)
        self.assertEqual(len(model.projections), 2)

        # Assert that the projection parameters have been parsed correctly
        self.assertEqual(model.projections[0].name, "PopA-PopB")
        self.assertEqual(model.projections[1].name, "InputA-PopA")

        # Assert that the correct populations are assigned to a projection
        self.assertEqual(model.projections[0].source, model.populations[0])
        self.assertEqual(model.projections[0].target, model.populations[1])
        self.assertEqual(model.projections[1].source, model.inputs[0])
        self.assertEqual(model.projections[1].target, model.populations[0])

    def testParseConnectionInstances(self):
        model = vicogen.parse_model("models/connection_instance_model.xml")

        # Assert number of populations and projections is correct
        self.assertEqual(len(model.populations), 2)
        self.assertEqual(len(model.projections), 1)

        # Assert number of neurons is correct
        self.assertEqual(model.populations[0].size(), 7)
        self.assertEqual(model.populations[1].size(), 8)

        self.assertTrue(isinstance(model.projections[0], nml.projections.InstancedConnections))

        # Assert number of connections is correct
        self.assertEqual(len(model.projections[0].connections), 10)

        # Assert a few connections
        self.assertEqual(model.projections[0].connections[1].con_id, "1")
        self.assertEqual(model.projections[0].connections[1].pre_cell_id, "1")
        self.assertEqual(model.projections[0].connections[1].post_cell_id, "3")

        self.assertEqual(model.projections[0].connections[7].con_id, "7")
        self.assertEqual(model.projections[0].connections[7].pre_cell_id, "6")
        self.assertEqual(model.projections[0].connections[7].post_cell_id, "0")

    def testParseSpatialConnectivity(self):
        model = vicogen.parse_model("models/spatial_connectivity_model.xml")

        self.assertEqual(model.projections[0]._mask.sigma, 1.5)
        self.assertEqual(model.projections[0]._mask.cutoff, 3)
