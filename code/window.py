import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from simulation import *
from functions import animation_text_save


class Window:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        self.results = ''


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


        menu_reactions = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Environmental Conditions',
            width=1280
        )

        # MENU REACTIONS
        menu_reactions.add.vertical_margin(50)
        # Reactions (Range slider) // pode-se alterar as bounds para text inputs de forma a alterar para 0,0 (com range slider não é possível)  
        
        for i in range(len(REACTIONS.name)):
            menu_reactions.add.range_slider(REACTIONS.name[i], (REACTIONS.lb[i],REACTIONS.ub[i]), (-1000, 1000), 10, font_size=30, rangeslider_id=REACTIONS.index[i]) #, rangeslider_id=OPTIONS['Reactions'][i])
        menu_reactions.add.vertical_margin(20)
        menu_reactions.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_reactions.add.vertical_margin(20)

        # MENU SUB (Genes)
        menu_genes.add.vertical_margin(50)
        label = '{}'

        for i in range(len(GENES)):
            txt = label.format(GENES[i])
            menu_genes.add.toggle_switch(txt, True, onchange=self.toggle_gene, kwargs=txt, toggleswitch_id=txt)
        menu_genes.add.vertical_margin(20)
        menu_genes.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_genes.add.vertical_margin(20)

        def run_simulation() -> None:
            """
            Run the simulation MEWPY.
            """
            try:
                menu.remove_widget(self.run_simul)
            except:
                pass
            animation_text_save('Running')
            self.results = run_simul()
            animation_text_save('Simulation Done')
            menu.add.button('Results', action=menu_simul, background_color=(0,150,50))
            print(type(self.results))
            # for i in self.results:
            #     print(i)


        menu_simul = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Run Simulation',
            width=1280
        )
        
        # menu_simul.add.button('Run Simulation', run_simulation)
        menu_simul.add.label("Results:")
        menu_simul.add.vertical_margin(50)  # Adds margin
        
        menu_simul.add.label(str(self.results))

        # menu_simul.add.button('Run Simulation', action=run_simulation, background_color=(0,150,50))
        menu_simul.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))

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
        menu_objective.add.range_slider('Fraction', default=90, range_values=(0,100), increment=1, rangeslider_id='obj_fraction')

        

        def data_fun() -> None:
            """
            Print data of the menu.
            """
            data_simul = menu.get_input_data()
            data_objective = menu_objective.get_input_data()
            data_genes = menu_genes.get_input_data()
            data_reac = menu_reactions.get_input_data()

            save_simulation_file([data_simul, data_objective, data_genes, data_reac])
            animation_text_save('Simulation saved')
            # self.run_simul = menu.add.button('Next', action=menu_simul, background_color=(0,150,50))
            self.run_simul = menu.add.button('Run Simulation', action=run_simulation, background_color=(0,150,50))
           


        def restore_data() -> None:
            """
            """
            menu.reset_value()
            menu_objective.reset_value()
            menu_genes.reset_value()
            menu_reactions.reset_value()
            # substituir simulation_file por simulation_file_initial (restaurar dados no ficheiro também)


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
        menu.add.button('Environmental Conditions', menu_reactions)
        menu.add.vertical_margin(50)  # Adds margin
        # menu.add.button('Restore Data', restore_data, background_color=(100,0,0))
        # menu.add.vertical_margin(20)  # Adds margin

        menu.add.button('Save Simulation', action=data_fun, background_color=(50,100,100))        
        menu.add.vertical_margin(20)  # Adds margin

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

