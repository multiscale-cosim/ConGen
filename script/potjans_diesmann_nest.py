import nest


import numpy as np

connectivityMap = [
        [ 0.101, 0.169, 0.044, 0.082, 0.032, 0.0,   0.008, 0.0,   0.0],
        [ 0.135, 0.137, 0.032, 0.052, 0.075, 0.0,   0.004, 0.0,   0.0],
        [ 0.008, 0.006, 0.050, 0.135, 0.007, 0.0003,0.045, 0.0,   0.0983],
        [ 0.069, 0.003, 0.079, 0.160, 0.003, 0.0,   0.106, 0.0,   0.0619],
        [ 0.100, 0.062, 0.051, 0.006, 0.083, 0.373, 0.020, 0.0,   0.0],
        [ 0.055, 0.027, 0.026, 0.002, 0.060, 0.316, 0.009, 0.0,   0.0],
        [ 0.016, 0.007, 0.021, 0.017, 0.057, 0.020, 0.040, 0.225, 0.0512],
        [ 0.036, 0.001, 0.003, 0.001, 0.028, 0.008, 0.066, 0.144, 0.0196],
        [ 0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0]
    ]

neuronModel = 'iaf_psc_alpha'
n_l23e =  20683
n_l23i =  5834 
n_l4e  =  21915
n_l4i  =  5479 
n_l5e  =  4850 
n_l5i  =  1065 
n_l6e  =  14395
n_l6i  =  2948 
n_th   =  902  

nFactor = 0.1

l23e = nest.Create(neuronModel, int(n_l23e * nFactor))
l23i = nest.Create(neuronModel, int(n_l23i * nFactor))
l4e = nest.Create(neuronModel, int(n_l4e * nFactor))
l4i = nest.Create(neuronModel, int(n_l4i * nFactor))
l5e = nest.Create(neuronModel, int(n_l5e * nFactor))
l5i = nest.Create(neuronModel, int(n_l5i * nFactor))
l6e = nest.Create(neuronModel, int(n_l6e * nFactor))
l6i = nest.Create(neuronModel, int(n_l6i * nFactor))
th = nest.Create(neuronModel, int(n_th * nFactor))

populations = [l23e,l23i,l4e,l4i,l5e,l5i,l6e,l6i,th]

for i, popSrc in enumerate(populations):
	for j, popTar in enumerate(populations):
		nest.Connect(popSrc, popTar, {'rule': 'pairwise_bernoulli', 'p': connectivityMap[i][j]})

print(len(nest.GetConnections()))