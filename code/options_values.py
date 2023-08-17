import mewpy
from mewpy.simulation import get_simulator

from cobra.io import read_sbml_model
model = read_sbml_model('../data/models/e_coli_core.xml.gz')
simul = get_simulator(model)
objective = simul.objective

METABOLITES = simul.find_metabolites() # dataframe
REACTIONS = simul.find_reactions() # dataframe
GENES_v0 = simul.find_genes().name # dataframe
COMPARTMENTS = list(simul.compartments) # dicionario

# MET = {name for (id_met, name) in METABOLITES.items()}
# REAC = {id_reac: name for (id_reac, name) in REACTIONS.items()}
GENES = [name for (name, _) in GENES_v0.items()]

# METABOLITES = simul.find_metabolites() # dataframe
# REACTIONS = simul.find_reactions() # dataframe
# GENES_v0 = simul.find_genes() # dataframe
# COMPARTMENTS = list(simul.compartments) # dicionario

# # MET = {name for (id_met, name) in METABOLITES.items()}
# # REAC = {id_reac: name for (id_reac, name) in REACTIONS.items()}
# GENES = [name for (name, _) in GENES_v0.items()]


OPTIONS = {
    'Metabolites': METABOLITES.name,
    'Reactions': REACTIONS.name,
    'Genes' : GENES,
    'Compartments': COMPARTMENTS,
    'Objective': objective
}

if __name__ == '__main__':
    # print(MET)
    # print(REAC)
    # for i in GENES.items():
    #     print(i)
    # print(len(GENES))
    # print(len(METABOLITES))
    # print(len(REACTIONS))
    # print(OPTIONS['Genes'])
    # print(OPTIONS['Metabolites'])
    # print(OPTIONS['Reactions'])
    print(REACTIONS)
    print(str(objective))
    # print(COMPARTMENTS)
    # for i in OPTIONS.values():
    #     print(i)
    # print(OPTIONS)
    # for i in range(len(OPTIONS['Metabolites'])):
    #     print(OPTIONS['Metabolites']['name'][i])
    # print(OPTIONS['Metabolites']['name'])

