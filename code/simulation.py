import mewpy
from cobra.io import read_sbml_model
from mewpy.simulation import get_simulator
from save_load import *
# from options_values import model
from options_values import *
#import file (model) here:

def run_simul():

    data_simul = load_file('player_history/simulation_file')
    # print(data_simul)

    method, objective, genes, reactions = data_simul

    method = method['method'][0][0]
    objective_name = objective['objective'][0][0]
    objective_fraction = objective['obj_fraction']

    # environment conditions:

    # envconditions = {'EX_glc__D_e': (-10.0, 100000.0),'EX_o2_e':(-1000,1000)}
    envconditions = {}

    # initial simulation:
    simul = get_simulator(model) #, envcond=envconditions)

    count = 0
    for i,(k, x) in enumerate(reactions.items()):
        if k == REACTIONS.index[count]:
            if simul.find_reactions().lb[count] != x[0] or simul.find_reactions().ub[count] != x[1]:
                    envconditions[k] = (x[0], x[1])
        else:
            count += 1
            if not x:
                envconditions[REACTIONS.index[count-1]] = (0, 0)

        

    for i,(k,x) in enumerate(genes.items()):
        if not x:
            print(k)
            
            # model.genes.k.knock_out()
            # envconditions[k] = 0

    # gene knockout:
    # model.genes.b4152.knock_out()

    # print(envconditions)

    # choose objective (by default Biomass):
    # objective = ''
    # simul.objective = objective

    # add constraints here (modifications on the game)
    constraints = {}
    constraints = envconditions
    # constraints = {'GND': 0, # deletion
    #                'PYK': 0, # deletion
    #                'ME2': 0, # deletion
    #               }

    # chooose simulation method (by default FBA):
    sim_method = method

    # run a simulation accounting with the new constraint
    result = simul.simulate(method=sim_method, constraints=constraints)

    # print(constraints)
    # print(result)
    # save_results(result)

    return str(result)

    # print(simul.objective)

    # print(result.fluxes['BIOMASS_Ecoli_core_w_GAM'])
    # print(result.fluxes['EX_succ_e'])

    # from mewpy.visualization.envelope import plot_flux_envelope
    # plot_flux_envelope(simul,'BIOMASS_Ecoli_core_w_GAM','EX_o2_e')



if __name__ == '__main__':

    import sys
    from time import sleep
    words = 'This is a test'
    for char in words:
        sleep(0.1)
        print(char, end='', flush=True)
    run_simul()