# CoGen

## Connectivity Generation Tool back end
ConGen is a tool to aid the generation of connectivity in multiscale and large scale neural networks.
The ConGen back end was created to interact with models generated with the ConGen front end (https://github.com/multiscale-cosim/NeuroScheme), generate the connectivity in the network and call different simulators to execute the selected model. Currently, ConGen supports models in NeuroML with specific extensions for connectivity patterns such as one-to-one and all-to-all. As simulator backends it supports NEST, TVB and is able to define the connectivity in scripts for co-simulation between NEST and TVB using the EBRAINS co-simulation infrastructure (https://github.com/multiscale-cosim/TVB-NEST).

### Python Module Structure

All of the python files are contained in a package named vicogen.
The NeuroML files are handled in the neuroml subpackage. 
The modules in the neuroml package are intended to hold the data structures of the translation and parsing NeuroML files. 
The module parsing.py contains all the functions for parsing NeuroML files into the data structures. 
The vicogen package itself contains a few different modules:

1. *\_vicogen.py* contains functions for accessing the file parsing from the *neuroml* package, starting simulations with NEST and printing connectivity matrices and lists to the console or to file. All of the functions in this module are made available on a package level. 
2. *nest.py* is the module responsible for connecting the translator to the simulator NEST. It provides functions for translating populations and calling the CGI-Functions for NEST, and also starting simulations.
3. *tvb.py* is the module responsible for connecting the translator to TVB. 
4. *\_\_main\_\_.py* is a required file for using the package by itself on a command line. It allows the package to be called like a module using *python -m ConGen PARAMETERS*.
5. *commands.py* provides the command arguments that can be used when calling the module from a command line. 
6. *\_\_init\_\_.py*  gathers all the functions from the other modules and provides them on a package level.

## Using ConGen
ConGen backend can be used independently of the front end (https://github.com/multiscale-cosim/NeuroScheme).
The ConGen package can be imported in Python using *import vicogen*.
Alternatively, ConGen can be used directly from the console by executing it as a Python module in the command line.

python -m vicogen [-h] [-o [OUTFILE]] [-t SIMTIME] [-c]
                  [-d] [-v] [-m multiscale] 
                  [-b simulate_with_tvb] 
                  [-n simulate_with_nest] 
                  [--nest-options NEST_OPTIONS]
                  [-l multiscale_labels]
                  modelfile
                    
                   
| Command | Description |    
| ----------- | ----------- |
|-h, --help  | Shows a help message on the usage. |
|-o [OUTFILE], --outfile [OUTFILE] | Set the file to write output to. If not given, the output is written to stdout. |
|-t SIMTIME, --SIMTIME | Simulate the model for a given amount of milliseconds. |
|-c, --write-connections | Instead of simulating the network, parse the connections and write them to output. |
|-n, --nest | Simulate with NEST. |
|--nest-options NEST\_OPTIONS | Additional options for NEST. |
|-b, --tvb | Simulate with TVB. |
|-m, --multiscale | Generate multiscale scripts (See also https://github.com/multiscale-cosim/TVB-NEST). |
|-l, --multiscale-labels | Labels to split the NeuroML model into scales. |
|-d, --debug |    Print debugging information. |
|-v, --verbose |    Print verbose messages. |

## Adding new simulators as target backends
New simulators can be added easily as all references to specific simulators are defined in thin layer scripts. Currently, such scripts for NEST and TVB are contained in the *nest.py* and *tvb.py* modules respectively. To create a new simulator think layer script:
1. Create the simulator script file <simulator>.py in the *python* folder.
2. Use the NeuroML network_model object to create the cells, connections and devices using the simulator-specific interface. This assumes that the simulator has a python interface. 
3. Add the required functions to call the simulator using the instantiated model.
4. Add a function in the *_vicogen.py* file with the following signature:
  build_<simulator>_model(model, options=None)
where model is the NeuroML network model, and the function generates the model acoording to the thin layer script <simulator>.py
5. Add a function in the *_vicogen.py* file with the following signature:
  simulate_<simulator>_model(model, sim_time=0.0, options=None)
where model is the NeuroML network model, and the function simulates the model acoording to the thin layer script <simulator>.py
6. Add a new argument to handle the new simulator in the *handle_arguments* function in the *_vicogen.py* file.

## Enriching simulator specific scripts
ConGen includes a set of basic launchers for NEST and TVB and a set of generators for co-simulation scripts.
All these scripts use default model and simulation parameters.
The user can extend the files nest.py and tvb.py to define model and simulation parameters using the specific simulator interface.
