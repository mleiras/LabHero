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
    # objective_fraction = objective['obj_fraction']

    envconditions = {}

    # initial simulation:
    simul = get_simulator(model) #, envcond=envconditions)


    reactions_original = simul.find_reactions('EX') # dataframe
    
    
    count = 0 # to access reactions
    count_2 = 0 # to access flow in and out inside each reaction (pair by pair)
    for i,(k,x) in enumerate(reactions.items()):
        if count_2 % 2 == 0: # if it's even, it means the toggle for the flow in
            envconditions[REACTIONS.index[count]] = (reactions_original.lb[count], reactions_original.ub[count])
            if not x:
                envconditions[REACTIONS.index[count]] = (0, envconditions[REACTIONS.index[count]][1])
            else:
                envconditions[REACTIONS.index[count]] = (-1000, envconditions[REACTIONS.index[count]][1])
            count_2 += 1
        else:
            if not x: # if it's uneven, it means the toggle for the flow out
                envconditions[REACTIONS.index[count]] = (envconditions[REACTIONS.index[count]][0], 0)
            else:
                envconditions[REACTIONS.index[count]] = (envconditions[REACTIONS.index[count]][0], 1000)
            count_2 += 1
            count += 1
        

    # print(envconditions)

    # REACTIONS WITH RANGE - deactivated
    # count = 0
    # for i,(k, x) in enumerate(reactions.items()):
    #     if k == REACTIONS.index[count]:
    #         if reactions_original.lb[count] != x[0] or reactions_original.ub[count] != x[1]:
    #             envconditions[k] = (x[0], x[1])
    #     else:
    #         count += 1
    #         if not x:
    #             envconditions[REACTIONS.index[count-1]] = (0, 0)


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
    results_str = str(result)
    # print(results_str)

    
    try:
        if str(results_str.splitlines()[1]) == 'Status: INFEASIBLE':
            results = 'Status: INFEASIBLE'
        else:
            results = round(float(str(results_str.splitlines()[0])[11:]), 3)
    except:
        results = results_str

    # print(result_str)

    # save_results(result)

    return objective_name, results

    # print(simul.objective)



if __name__ == '__main__':
     print(run_simul())
    