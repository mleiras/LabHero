import mewpy
from mewpy.simulation import get_simulator

from cobra.io import read_sbml_model
model = read_sbml_model('../data/models/e_coli_core.xml.gz')
simul = get_simulator(model)

METABOLITES = simul.find_metabolites().name # dataframe
REACTIONS = simul.find_reactions().name # dataframe
GENES = simul.find_genes().name # dataframe
COMPARTMENTS = list(simul.compartments) # dicionario

MET = {id_met: name for (id_met, name) in METABOLITES.items()}

REAC = {id_reac: name for (id_reac, name) in REACTIONS.items()}


OPTIONS = {
    'Metabolites': METABOLITES[:10],
    'Reactions': REACTIONS[:10],
    'Genes' : GENES,
    'Compartments': COMPARTMENTS
}

if __name__ == '__main__':
    print(MET)
    print(REAC)
    print(GENES)
    print(COMPARTMENTS)
