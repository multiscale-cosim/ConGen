# This file is a modification from https://github.com/multiscale-cosim/TVB-NEST/blob/master/nest_elephant_tvb/translation/nest_to_tvb.py
# Which is in charge of generating the translation module from nest to tvb in the multiscale simulation framework of EBRAINS.

#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0. "

import nest
import numpy

from . import neuroml

import os
import json
import logging
import sys

import nest_elephant_tvb.translation.RichEndPoint as REP
import nest_elephant_tvb.translation.transformer_nest_tvb as tnt

def create_logger(path,name, log_level):
    # Configure logger
    logger = logging.getLogger(name)
    fh = logging.FileHandler(path+'/log/'+name+'.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if log_level == 0:
        fh.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    elif  log_level == 1:
        fh.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
    elif  log_level == 2:
        fh.setLevel(logging.WARNING)
        logger.setLevel(logging.WARNING)
    elif  log_level == 3:
        fh.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
    elif  log_level == 4:
        fh.setLevel(logging.CRITICAL)
        logger.setLevel(logging.CRITICAL)

    return logger

class NTTTranslatorModel:

    def __init__(self, a1, a3, network_model):
   	############ Step 1: all argument parsing stuff
  	self.path = a1
  	nest_to_tvb = ""
  	for input_ in network_model.inputs:
   	   if input_.name == "SpikeToRate_":
   	       nest_to_tvb = input_.id
    	if not nest_to_tvb:
        	logging.error("No translator defined")
        	sys.exit(1)
   	self.file_spike_detector = nest_to_tvb
    	self.TVB_recev_file = a3
   	# take the parameters and instantiate objects for analysing data
    	with open(path+'/parameter.json') as f:
        	parameters = json.load(f)
    	self.param = parameters['param_TR_nest_to_tvb']
   	#############
    
    	############ Step 2: init all loggers.
    	### TODO: use proper logging interface 
    	### -> https://github.com/multiscale-cosim/TVB-NEST/tree/master/configuration_manager
    	level_log = param['level_log']
    	self.id_spike_detector = os.path.splitext(os.path.basename(path+file_spike_detector))[0]
    	self.logger_master = create_logger(path, 'nest_to_tvb_master'+str(id_spike_detector), level_log)
    	self.logger_receive = create_logger(path, 'nest_to_tvb_receive'+str(id_spike_detector), level_log)
    	self.logger_send = create_logger(path, 'nest_to_tvb_send'+str(id_spike_detector), level_log)
    	#############

    def run_translator(self):
    
    	############ Step 3: RichEndPoint -- open MPI connections
    	### TODO: make this a proper interface
    	path_to_files_receive = self.path + self.file_spike_detector # TODO: use proper path operations
    	path_to_files_send = self.path + self.TVB_recev_file
    	comm, comm_receiver, port_receive, comm_sender, port_send = REP.make_connections(path_to_files_receive, path_to_files_send, logger_master)
    	#############
    
    	############ Step 4: MPI Transformer, init and start the co-simulation
    	### TODO: encapsulate loggers, kept all logging stuff here for now to have them in one place
    	### TODO: split Transformer its sub-tasks: RichEndPoint, Transformation, Science
   	loggers = [self.logger_master, self.logger_receive, self.logger_send] # list of all the loggers
    	tnt.init(self.path, self.param, comm, comm_receiver, comm_sender, loggers)
    	############
    
   	############ Step 5: RichEndPoint -- close MPI connections
    	### TODO: make this a proper interface
    	REP.close_and_finalize(port_send, port_receive,logger_master)
    	############
    
    	############ Step 6: cleanup, delete files
    	### TODO: ugly solution, all MPI ranks want to delete, only the first one can.
    	self.logger_master.info('clean file')
    	try:
    	    os.remove(self.path_to_files_receive)
        	os.remove(self.path_to_files_send)
    	except FileNotFoundError:
        	pass 
    	self.logger_master.info('end')
    	############

def nest_to_tvb_build_translator(a1, a3, network_model, options=None):
    translator_model = NTTTranslatorModel(a1, a3, network_model)
    return translator_model

