import mewpy
from cobra.io import read_sbml_model
from mewpy.simulation import get_simulator
from save_load import *
from options_values import *

def run_simul():

    data_simul = load_file(get_resource_path('code/player_history/simulation_file'))

    method, objective, genes, reactions = data_simul

    method = method['method'][0][0]
    objective_name = objective['objective'][0][0]
    objective_fraction = objective['obj_fraction']

    envconditions = {}

    # initial simulation:
    simul = get_simulator(model) #, envcond=envconditions)

    reactions_original = simul.find_reactions('EX') # dataframe

    count = 0
    for i,(k, x) in enumerate(reactions.items()):
        if k == REACTIONS.index[count]:
            if reactions_original.lb[count] != x[0] or reactions_original.ub[count] != x[1]:
                envconditions[k] = (x[0], x[1])
        else:
            count += 1
            if not x:
                envconditions[REACTIONS.index[count-1]] = (0, 0)


    for i,(k,x) in enumerate(genes.items()):
        if not x:
            # print(k)
            # print(simul.find_genes().reactions[i])
            list_react = simul.find_genes().reactions[i]
            for react in list_react:
                envconditions[react] = (0,0)

    # gene knockout:
    # model.genes.b1524.knock_out()


    # print(envconditions)

    # choose objective (by default Biomass):
    # objective = ''
    simul.objective = objective_name

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



if __name__ == '__main__':
     print(run_simul())
    