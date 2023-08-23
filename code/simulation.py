import mewpy
from cobra.io import read_sbml_model
from mewpy.simulation import get_simulator
from save_load import *

#import file (model) here:
model = read_sbml_model('../data/models/iML1515.xml.gz') #'.../data/models/iML1515.xml'

data_simul = load_file('simulation_file')
# print(data_simul)

method, objective, genes, reactions = data_simul

method = method['method'][0][0]
objective_name = objective['objective'][0][0]
objective_fraction = objective['obj_fraction']

# print(reactions)


# environment conditions:
envconditions = {'EX_glc__D_e': (-10.0, 100000.0),
           'EX_o2_e':(-1000,1000)}

# initial simulation:
simul = get_simulator(model) #, envcond=envconditions)

# choose objective (by default Biomass):
# objective = ''
# simul.objective = objective

# add constraints here (modifications on the game)
constraints = {}
# constraints = {'GND': 0, # deletion
#                'PYK': 0, # deletion
#                'ME2': 0, # deletion
#               }

# chooose simulation method (by default FBA):
sim_method = method


# run a pFBA simulation accounting with the new constraint
result = simul.simulate(method=sim_method, constraints=constraints)

print(result)

# print(result.fluxes['BIOMASS_Ecoli_core_w_GAM'])
# print(result.fluxes['EX_succ_e'])


# from mewpy.visualization.envelope import plot_flux_envelope
# print(plot_flux_envelope(simul,'BIOMASS_Ecoli_core_w_GAM','EX_succ_e'))
