import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save


class Window:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        
        self.index = 0
        self.timer = Timer(200)



    def setup(self):
        
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Simulation Menu',
            width=1280,
        )

        menu_genes = pygame_menu.Menu(
            height=720,
            center_content=False,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Genes',
            width=1280
        )

        menu_met = pygame_menu.Menu(
            height=720,
            center_content=False,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Metabolites',
            width=1280,
        )


        menu_contributors = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Contributors',
            width=1280
        )

        # Add table to contributors
        table_contrib = menu_contributors.add.table()
        table_contrib.default_cell_padding = 5
        table_contrib.default_row_background_color = 'grey'
        bold_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        table_contrib.add_row(['Nº', 'Github User'], cell_font=bold_font)
        for i in range(len(pygame_menu.__contributors__)):
            table_contrib.add_row([i + 1, pygame_menu.__contributors__[i]], cell_font=bold_font if i == 0 else None)

        table_contrib.update_cell_style(-1, -1, font_size=15)  # Update all column/row
        table_contrib.update_cell_style(1, [2, -1], font=pygame_menu.font.FONT_OPEN_SANS_ITALIC)


        menu_reactions = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Reactions',
            width=1280
        )

        # MENU REACTIONS
        menu_reactions.add.vertical_margin(50)
        # Reactions (Range slider) // pode-se alterar as bounds para text inputs de forma a alterar para 0,0 (com range slider não é possível)  
        for i in range(len(OPTIONS['Reactions'])):
            # menu_reactions.add.label(f'Reaction {OPTIONS["Reactions"][i]}', font_size=18)
            menu_reactions.add.range_slider(OPTIONS["Reactions"][i], (REACTIONS.lb[i],REACTIONS.ub[i]), (-1000, 1000), 10, font_size=30, rangeslider_id=REACTIONS.index[i]) #, rangeslider_id=OPTIONS['Reactions'][i])
            # menu_reactions.add.range_slider('LB', REACTIONS.lb[i], (-1000, 1000), 10, font_size=15) #, rangeslider_id=OPTIONS['Reactions'][i])
            # menu_reactions.add.range_slider('UP', REACTIONS.ub[i], (-1000, 1000), 10, font_size=16) #, rangeslider_id=OPTIONS['Reactions'][i])
        menu_reactions.add.vertical_margin(20)
        menu_reactions.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_reactions.add.vertical_margin(20)

        # MENU SUB (Genes)
        menu_genes.add.vertical_margin(50)
        label = '{}'

        for i in range(len(OPTIONS['Genes'])):
            txt = label.format(OPTIONS['Genes'][i])
            menu_genes.add.toggle_switch(txt, True, onchange=self.toggle_gene, kwargs=txt, toggleswitch_id=txt)
        menu_genes.add.vertical_margin(20)
        menu_genes.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_genes.add.vertical_margin(20)

        # MENU SUB METABOLITES
        menu_met.add.vertical_margin(50)
        menu_met.add.label(f'Compartments:', font_size=30,font_color=(70, 70, 70))
        for k,v in COMPARTMENTS.items():
            menu_met.add.label(f'{k}: {v}', font_size=25, font_color=(70, 70, 70))
        menu_met.add.vertical_margin(20)
        label = '{}'
        for i in range(len(METABOLITES['name'])):
            texto = str(METABOLITES['name'][i])+' - '+str(METABOLITES['compartment'][i])
            # txt = label.format(METABOLITES['name'][i])
            menu_met.add.toggle_switch(texto, True, onchange=self.toggle_gene, kwargs=texto, toggleswitch_id=METABOLITES.index[i])
        menu_met.add.vertical_margin(20)
        menu_met.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_met.add.vertical_margin(20)

        # MENU SUB OBJECTIVE
        menu_objective = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Objective',
            width=1280
        )

        objectives = []
        default_obj = 0
        # print(str(objective))
        
        for i in range(len(REACTIONS)):
            if REACTIONS.index[i] == str(objective):
                default_obj = i
            objectives.append((REACTIONS.index[i], REACTIONS.index[i]))
        
        menu_objective.add.dropselect(title='Objective: ',
                            items=objectives,
                                   default=default_obj,
                                   selection_box_height=8,
                                   selection_box_width=500,
                                   dropselect_id='objective')

        
        def run_simulation() -> None:
            """
            Run the simulation MEWPY.
            """
            menu.remove_widget(self.run_simul)
            print('RUN SIMULATION')
            # add mewpy script here to run new simulation
            animation_text_save('Simulation Running')
            #close menu here?


        def data_fun() -> None:
            """
            Print data of the menu.
            """
            data_simul = menu.get_input_data()
            data_objective = menu_objective.get_input_data()
            data_genes = menu_genes.get_input_data()
            data_met = menu_met.get_input_data()
            data_reac = menu_reactions.get_input_data()

            save_simulation_file([data_simul, data_objective, data_genes, data_met, data_reac])
            animation_text_save('Simulation saved')
            self.run_simul = menu.add.button('Run Simulation', action=run_simulation, background_color=(150,50,50))
            self.run_simul

       

        menu.add.dropselect(title='Simulation Method: ',
                            items=[('FBA', 'fba'),
                                   ('pFBA', 'pfba'),
                                   ('MOMA', 'moma'),
                                   ('lMOMA', 'lmoma'),
                                   ('ROOM','room')],
                                   default=0,
                                   selection_box_height=4, dropselect_id='method')
        # menu.add.text_input('Objective: ', default=str(OPTIONS['Objective']), textinput_id='objective')
        menu.add.button('Objective', menu_objective)
        menu.add.button('Genes', menu_genes)
        menu.add.button('Metabolites', menu_met)
        # menu.add.button('Table', menu_contributors)
        menu.add.button('Reactions', menu_reactions)
        menu.add.vertical_margin(50)  # Adds margin
        menu.add.button('Save Simulation', action=data_fun, background_color=(50,100,100))        
        menu.add.vertical_margin(20)  # Adds margin
        # menu.add.button('Restore / Cancel', menu.reset_value, background_color=(100,0,0))

        menu.mainloop(self.display_surface)

        


    def toggle_menu(self):
        self.desk_menu = not self.desk_menu


    
    def on_button_click(self, value: str, text = None) -> None:
        if not text:
            print(f'Hello from {value}')
        else:
            print(f'Hello from {text} with {value}')


    def toggle_gene(self, txt, **id) -> None:
        """
        Button event on menus.

        :param value: Button value
        :param text: Button text
        """
        if txt:
            print(f'{id} on')
        else:
            print(f'{id} knockout')



    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        


