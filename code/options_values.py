import mewpy
from mewpy.simulation import get_simulator

from cobra.io import read_sbml_model
model = read_sbml_model('../data/models/e_coli_core.xml.gz')
simul = get_simulator(model)


METABOLITES = simul.find_metabolites().name # dataframe
REACTIONS = simul.find_reactions().name # dataframe
GENES_v0 = simul.find_genes().name # dataframe
COMPARTMENTS = list(simul.compartments) # dicionario

MET = {name for (id_met, name) in METABOLITES.items()}

REAC = {id_reac: name for (id_reac, name) in REACTIONS.items()}

GENES = [name for (name, _) in GENES_v0.items()]


OPTIONS = {
    'Metabolites': METABOLITES[:20],
    'Reactions': REACTIONS[:10],
    'Genes' : GENES,
    'Compartments': COMPARTMENTS
}

if __name__ == '__main__':
    # print(MET)
    # print(REAC)
    # for i in GENES.items():
    #     print(i)
    print(len(GENES))
    # print(METABOLITES)
    # print(REACTIONS)
    print(GENES_v0[0].is_active())
    # print(COMPARTMENTS)
    # for i in OPTIONS.values():
    #     print(i)
    # print(OPTIONS)
