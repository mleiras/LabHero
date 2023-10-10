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
mytheme.widget_font_color = 'black'
# mytheme.background_color=(255,215,0, 255) #gold #transparency 100% = 255
# mytheme.background_color=(150,190,140)

tutorial_theme = mytheme.copy()
tutorial_theme.background_color = (255,215,0, 255)


from cobra.io import read_sbml_model
model = read_sbml_model('../data/models/e_coli_core.xml.gz') #('.../data/models/iMM904.xml.gz') #('../data/models/e_coli_core.xml.gz')
# model = read_sbml_model('.../data/models/iML1515.xml.gz')
simul = get_simulator(model)
objective = list(simul.objective.keys())[0]

# METABOLITES = simul.find_metabolites() # dataframe
# COMPARTMENTS = simul.compartments # dicionario
REACTIONS_v0 = simul.find_reactions()
REACTIONS = simul.find_reactions('EX') # dataframe

GENES_v0 = simul.find_genes().name # dataframe
GENES = [name for (name, _) in GENES_v0.items()]


if __name__ == '__main__':
    
    print(GENES)
    # print(REACTIONS)
    print(REACTIONS_v0)
    print(simul.find_reactions('EX_etoh_e'))
    # print(simul.essential_genes())
    # print(simul.find_genes().reactions)
    # print(simul.find_reactions().index['dhaK'])
    
    