import mewpy
from mewpy.simulation import get_simulator
import pygame_menu

mytheme = pygame_menu.themes.THEME_GREEN.copy()
font = pygame_menu.font.FONT_MUNRO
mytheme.widget_font = font
mytheme.title_font = font
mytheme.title_font_size = 50
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
mytheme.title_offset = (20,4)
mytheme.widget_margin = (10,10)


from cobra.io import read_sbml_model
model = read_sbml_model('../data/models/e_coli_core.xml.gz')
simul = get_simulator(model)
objective = simul.objective

METABOLITES = simul.find_metabolites() # dataframe
REACTIONS = simul.find_reactions() # dataframe
GENES_v0 = simul.find_genes().name # dataframe
COMPARTMENTS = simul.compartments # dicionario

# if len(COMPARTMENTS) > 1:
#     print('teste')

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
    # print(REACTIONS)
    # print(str(objective))
    # print(OPTIONS['Metabolites'])
    # for i in OPTIONS.values():
    #     print(i)
    print(COMPARTMENTS)
    # for i in range(len(OPTIONS['Metabolites'])):
    #     print(METABOLITES['compartment'][i])
    # print(OPTIONS['Metabolites']['name'])
    for k,v in COMPARTMENTS.items():
        print(k)
        print(v)

