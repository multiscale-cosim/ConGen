import neuroml
import logging
import numpy as np
import numpy.random as rgn
import math
from string import Template

def build_translator_file(nest_model, options=None):
    
    with open("./vicogen/_run_mpi_nest_to_tvb_template.sh", 'r') as tempfile:
        with open("./vicogen/_run_mpi_nest_to_tvb_ConGen.sh", 'w+') as outfile:
            t = Template(tempfile.read())
            sub = str(nest_model.id_spike_to_rate[0])
            s = t.safe_substitute(id_spk_to_rt="{}".format(sub))
            outfile.write(s)
    with open("./vicogen/_run_mpi_tvb_to_nest_template.sh", 'r') as tempfile:
        with open("./vicogen/_run_mpi_tvb_to_nest_ConGen.sh", 'w+') as outfile:
            t = Template(tempfile.read())
            sub = str(nest_model.id_spike_to_rate[0])
            cnt = str(nest_model.nr_spike_to_rate)
            s = t.safe_substitute(id_spk_to_rt="{}".format(sub), count_trans="{}".format(cnt))
            outfile.write(s)
