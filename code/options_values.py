import mewpy
from mewpy.simulation import get_simulator
import pygame_menu
from save_load import *

mytheme = pygame_menu.themes.THEME_GREEN.copy() #(186,214,177)
font = pygame_menu.font.FONT_MUNRO
mytheme.widget_font = font
mytheme.title_font = font
mytheme.title_font_size = 50
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
mytheme.title_offset = (20,4)
mytheme.widget_margin = (10,10)
# mytheme.background_color=(255,215,0, 255) #gold #transparency 100% = 255
mytheme.background_color=(150,190,140)



# data_simul = load_file('simulation_file')
# method, objective, genes, reactions = data_simul

# objective_name = objective['objective'][0][0]
# objective_fraction = objective['obj_fraction']

# REACTIONS = reactions
# GENES = genes

from cobra.io import read_sbml_model
model = read_sbml_model('../data/models/e_coli_core.xml.gz') #('.../data/models/iMM904.xml.gz') #('../data/models/e_coli_core.xml.gz')
# model = read_sbml_model('../data/models/iML1515.xml.gz')
simul = get_simulator(model)
objective = list(simul.objective.keys())[0]


METABOLITES = simul.find_metabolites() # dataframe
REACTIONS = simul.find_reactions() # dataframe
GENES_v0 = simul.find_genes().name # dataframe
COMPARTMENTS = simul.compartments # dicionario

GENES = [name for (name, _) in GENES_v0.items()]


# OPTIONS = {
#     'Metabolites': METABOLITES.name,
#     'Reactions': REACTIONS.name,
#     'Genes' : GENES,
#     'Compartments': COMPARTMENTS,
#     'Objective': objective
# }

if __name__ == '__main__':
    
    # print(COMPARTMENTS)
    print(GENES)
    # print(METABOLITES)
    print(REACTIONS)
    