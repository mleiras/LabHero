import mewpy
from cobra.io import read_sbml_model
from mewpy.simulation import get_simulator

#import file (model) here:
model = read_sbml_model('../data/models/e_coli_core.xml.gz')



# environment conditions:
envconditions = {'EX_glc__D_e': (-10.0, 100000.0),
           'EX_o2_e':(0,0)}

# initial simulation:
simul = get_simulator(model, envcond=envconditions)

# choose objective (by default Biomass):
# objective = ''
# simul.objective = objective
simul.objective='BIOMASS_Ecoli_core_w_GAM'

# add constraints here (modifications on the game)
constraints = {}
constraints = {'GND': 0, # deletion
               'PYK': 0, # deletion
               'ME2': 0, # deletion
              }

# chooose simulation method (by default FBA):
sim_method = 'pFBA'


# run a pFBA simulation accounting with the new constraint
result = simul.simulate(method=sim_method, constraints=constraints)

print(result)

# print(result.fluxes['BIOMASS_Ecoli_core_w_GAM'])
# print(result.fluxes['EX_succ_e'])


# from mewpy.visualization.envelope import plot_flux_envelope
# print(plot_flux_envelope(simul,'BIOMASS_Ecoli_core_w_GAM','EX_succ_e'))
