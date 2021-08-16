import numpy as np
import csa.valueset


class Distribution:
    def __init__(self):
        pass

    def sample(self, n=None):
        """

        :param n:
        :return: A sample from the distribution
        :rtype: float
        """
        raise NotImplementedError("Class %s doesn't implement sample()" % self.__class__.__name__)

    def vset(self):
        """

        :rtype: csa.valueset.ValueSet|float
        """
        return csa.valueset.GenericValueSet(lambda i, j: float(self.sample()))


class UniformDistribution(Distribution):
    def __init__(self, lower, upper):
        Distribution.__init__(self)
        self.lower = lower
        self.upper = upper

    def sample(self, n=None):
        if n is None:
            return np.random.uniform(self.lower, self.upper).astype(float)
        else:
            return np.random.uniform(self.lower, self.upper, n)


class GaussianDistribution(Distribution):
    def __init__(self, mu=0.0, sigma=1.0):
        Distribution.__init__(self)
        self.mu = mu
        self.sigma = sigma

    def sample(self, n=None):
        if n is None:
            return np.random.normal(self.mu, self.sigma).astype(float)
        else:
            return np.random.normal(self.mu, self.sigma, n)
