import unittest
import random
import numpy as np

import vicogen
import vicogen.neuroml as nml


class ConnectivityTest(unittest.TestCase):
    def setUp(self):
        self.popASize = 10
        self.popBSize = 5

        self.popA = nml.populations.PopulationTemplate("PopA", self.popASize, 'iaf_psc_alpha')
        self.popB = nml.populations.PopulationTemplate("PopB", self.popBSize, 'iaf_psc_alpha')
        self.synprops = nml.synapses.SynapseProperties(10.0, 0.5, nml.synapses.SynapseModel('static_synapse'))

    def testAllToAll(self):
        proj = nml.projections.AllToAll("AllToAll", self.popA, self.popB, self.synprops)
        connmat = nml.get_connectivity_matrix(proj)

        controlmat = np.ones((self.popASize, self.popBSize))
        np.testing.assert_array_equal(connmat, controlmat)

    def testOneToOne(self):
        proj = nml.projections.OneToOne("OneToOne", self.popA, self.popB, self.synprops)
        connmat = nml.get_connectivity_matrix(proj)

        controlmat = np.fromfunction(lambda i, j: i == j, (self.popASize, self.popBSize), dtype=np.float)
        np.testing.assert_array_equal(connmat, controlmat)

    def testRandom(self):
        random.seed(42)

        proj = nml.projections.FixedProbability(0.1, "Random", self.popA, self.popB, self.synprops)

        connmat = nml.get_connectivity_matrix(proj)

        controlmat = np.array([[0., 0., 0., 0., 0.],
                               [1., 0., 0., 0., 1.],
                               [0., 1., 0., 0., 0.],
                               [0., 0., 0., 0., 0.],
                               [0., 0., 0., 0., 1.],
                               [0., 0., 0., 0., 0.],
                               [0., 0., 1., 0., 0.],
                               [1., 0., 1., 0., 0.],
                               [0., 0., 0., 0., 0.],
                               [1., 1., 0., 0., 0.]])

        np.testing.assert_array_equal(connmat, controlmat)

    def testFanIn(self):
        random.seed(42)

        proj = nml.projections.PerCell(3, "Random", self.popA, self.popB, self.synprops)

        connmat = nml.get_connectivity_matrix(proj)

        controlmat = np.array([[1., 1., 0., 1., 0.],
                               [0., 1., 0., 2., 0.],
                               [1., 0., 1., 0., 1.],
                               [1., 1., 1., 0., 0.],
                               [2., 0., 0., 1., 0.],
                               [0., 1., 2., 0., 0.],
                               [1., 0., 0., 0., 2.],
                               [1., 1., 0., 1., 0.],
                               [1., 1., 0., 0., 1.],
                               [1., 0., 0., 1., 1.]])

        np.testing.assert_array_equal(connmat, controlmat)

    def testFanOut(self):
        random.seed(42)

        proj = nml.projections.PerCell(3, "Random", self.popA, self.popB, self.synprops, reverse=True)

        connmat = nml.get_connectivity_matrix(proj)

        controlmat = np.array([[1., 0., 1., 1., 1.],
                               [0., 0., 0., 0., 1.],
                               [1., 1., 0., 1., 0.],
                               [0., 0., 0., 0., 0.],
                               [0., 0., 1., 0., 0.],
                               [0., 0., 0., 1., 0.],
                               [1., 1., 0., 0., 1.],
                               [0., 1., 0., 0., 0.],
                               [0., 0., 1., 0., 0.],
                               [0., 0., 0., 0., 0.]])

        np.testing.assert_array_equal(connmat, controlmat)


if __name__ == '__main__':
    unittest.main()
