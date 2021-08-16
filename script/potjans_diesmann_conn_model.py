import json
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

# List populations
populations = []

populations.append({'name': 'l23e', 'size': n_l23e, 'neuronModel': neuronModel})
populations.append({'name': 'l23i', 'size': n_l23i, 'neuronModel': neuronModel})
populations.append({'name': 'l4e',  'size': n_l4e,  'neuronModel': neuronModel})
populations.append({'name': 'l4i',  'size': n_l4i,  'neuronModel': neuronModel})
populations.append({'name': 'l5e',  'size': n_l5e,  'neuronModel': neuronModel})
populations.append({'name': 'l5i',  'size': n_l5i,  'neuronModel': neuronModel})
populations.append({'name': 'l6e',  'size': n_l6e,  'neuronModel': neuronModel})
populations.append({'name': 'l6i',  'size': n_l6i,  'neuronModel': neuronModel})
populations.append({'name': 'th',   'size': n_th,   'neuronModel': neuronModel})

# Generate connections from connectivityMap
connections = []
for indexFrom, popFrom in enumerate(populations):
    for indexTo, popTo in enumerate(populations):
        connectivity = connectivityMap[indexTo][indexFrom]
        
        if connectivity <= 0.0:
            continue

        connections.append({'source': popFrom['name'], 'target': popTo['name'], 'connectivityModel': 'random', 'connectivity': connectivity})

# Create Inputs
inputConnections = [1600, 1500, 2100, 1900, 2000, 1900, 2900, 2100, 0]
inputs = []
for inputConnection, population in zip(inputConnections, populations):
    if inputConnection <= 0:
        continue
    inputs.append({'inputType': 'poisson', 'target': population['name'], 'n': inputConnection})

model_dict = {'populations': populations, 'connections': connections, 'inputs': inputs}

with open("potjans_diesmann_conn_model.json", 'w') as fp:
    json.dump(model_dict, fp, indent=4)