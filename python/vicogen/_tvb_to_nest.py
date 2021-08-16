# This file is a modification from https://github.com/multiscale-cosim/TVB-NEST/blob/master/nest_elephant_tvb/translation/tvb_to_nest.py
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
import nest_elephant_tvb.translation.transformer_tvb_nest as ttn

def create_logger(path,name, log_level):
    # Configure logger
    logger = logging.getLogger(name)
    fh = logging.FileHandler(path+'/../../log/'+name+'.log')
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


class TTNTranslatorModel:
    def __init__(self, a1, a3, a4, network_model):

    	############ Step 1: all argument parsing stuff
    	self.path_config = a1
    	for input_ in network_model.inputs:
        	if input_.name == "RateToSpike_":
            	tvb_to_nest = input_.id
    	if not tvb_to_nest:
        	logging.error("No translator defined")
        	sys.exit(1)
    	
    	self.id_first_spike_detector = int(tvb_to_nest)
    	self.nb_spike_generator = int(a3)
    	self.TVB_config = a4
    	# take the parameters and instantiate objects for analysing data
    	with open(path_config+'/../../parameter.json') as f:
        	parameters = json.load(f)
    	self.param = parameters['param_TR_tvb_to_nest']
    	############
    
    	############ Step 2: init all loggers.
    	### TODO: use proper logging interface 
    	### -> https://github.com/multiscale-cosim/TVB-NEST/tree/master/configuration_manager

    	self.log_level = param['level_log']
    	self.logger_master = create_logger(path_config, 'tvb_to_nest_master'+str(id_first_spike_detector), log_level)
    	self.logger_send = create_logger(path_config, 'tvb_to_nest_send'+str(id_first_spike_detector), log_level)
    	self.logger_receive = create_logger(path_config, 'tvb_to_nest_receive'+str(id_first_spike_detector), log_level)
    	############
   
    def run_translator(self):
    	############ Step 3: RichEndPoint -- open MPI connections
    	### TODO: make this a proper interface
    	path_to_files_receive = self.path_config + self.TVB_config
    	path_to_files_send = os.path.join(self.path_config, str(self.id_first_spike_detector) + ".txt")
    	comm, comm_receiver, port_receive, comm_sender, port_send = REP.make_connections(self.path_to_files_receive, self.path_to_files_send, self.logger_master)
    	'''
    	# TODO: why is the loop needed, could not see where this is ever reused.
    	# TODO: only path/output/0.txt is
    	for i in range(nb_spike_generator):
        	# write file with port and unlock
        	path_to_files_send = os.path.join(path_config, str(id_first_spike_detector+i) + ".txt")
        	fport_send = open(path_to_files_send, "w+")
        	fport_send.write(port_send)
        	fport_send.close()
        	path_to_files_send_unlock = os.path.join(path_config, str(id_first_spike_detector+i) + ".txt.unlock")
        	pathlib.Path(path_to_files_send_unlock).touch()
        	path_to_files_sends.append(path_to_files_send)
        	path_to_files_sends_unlock.append(path_to_files_send_unlock)
    	'''
    	############
    
    	############ Step 4: MPI Transformer, init and start the co-simulation
    	### TODO: encapsulate loggers, kept all logging stuff here for now to have them in one place
    	### TODO: split Transformer its sub-tasks: RichEndPoint, Transformation, Sciences
    	### TODO: looong parameter list. Do this properly after merging with the launcher from Rolando
    	loggers = [self.logger_master, self.logger_receive, self.logger_send] # list of all the loggers
    	ttn.init(self.path_config, self.nb_spike_generator, self.id_first_spike_detector, self.param,
            	comm, comm_receiver, comm_sender, loggers)
    	############
    
    	############ Step 5: RichEndPoint -- close MPI connections
    	### TODO: make this a proper interface
    	REP.close_and_finalize(self.port_send, self.port_receive,self.logger_master)
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

def tvb_to_nest_build_translator(a1, a3, a4, network_model, options=None):
    translator_model = TTNTranslatorModel(a1, a3, a4, network_model)
    return translator_model

