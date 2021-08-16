This folder contains scripts for the ontology translation

___

csa_from_json.py

This file reads a json file of a model, converts the connectivity into CSA and tries to simulate it in NEST. Use it like `python csa_from_json.py model_file.json`.

____

potjans_diesmann_conn_model.json

This file contins the connectivity model of the local cortical network as described in Potjans, Diesmann (2011).

____

potjans_diesmann_conn_model.py

This script creates the potjans_diesmann_conn_model.json file.

____

csa_misc_functions.py

This script contains some useful helper functions when working with CSA.