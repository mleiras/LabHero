import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from simulation import *
from functions import animation_text_save


class Window:
    def __init__(self, toggle_menu, player) -> None:

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path,30)
        self.results = ''

        # self.index = 0
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
            menu_reactions.add.range_slider(REACTIONS.name[i], (REACTIONS.lb[i],REACTIONS.ub[i]), (-1000, 1000), 10, font_size=30, range_box_color = 'gold', rangeslider_id=REACTIONS.index[i]) #, rangeslider_id=OPTIONS['Reactions'][i])
            menu_reactions.add.toggle_switch('Bounds',True, onchange=None, state_text=('Deactivated', 'Active'), state_text_font_size=20, font_size = 24, state_color=('grey','gold')) #, kwargs=txt, toggleswitch_id=txt)
            menu_reactions.add.vertical_margin(30)
        menu_reactions.add.vertical_margin(20)
        menu_reactions.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_reactions.add.vertical_margin(20)

        # def toggle_reaction(txt, **id):
        #     if not txt:
        #         REACTIONS.lb[i] = 0
        #         REACTIONS.ub[i] = 0
        #     else:
        #         pass

        # MENU SUB (Genes)
        menu_genes.add.vertical_margin(50)
        label = '{}'

        for i in range(len(GENES)):
            txt = label.format(GENES[i])
            menu_genes.add.toggle_switch(txt, True, kwargs=txt, toggleswitch_id=txt)
        menu_genes.add.vertical_margin(20)
        menu_genes.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_genes.add.vertical_margin(20)


        # MENU RESULTS
        menu_results = pygame_menu.Menu(
            height=720,
            onclose=pygame_menu.events.BACK,
            theme=mytheme,
            title='Last Results',
            width=1280
        )
        menu_results.add.vertical_margin(20)
        try:
            res_path = get_resource_path('code/player_history/results')
            res = load_file(res_path)

            menu_results.add.label(res)
        except FileNotFoundError:
            menu_results.add.label('You have to make at least one simulation to see results.')


        
        

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
        
        for i in range(len(REACTIONS_v0)):
            if REACTIONS_v0.index[i] == str(objective):
                default_obj = i
            objectives.append((REACTIONS_v0.index[i], REACTIONS_v0.index[i]))
        
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
            animation_text_save('Running')
            self.results = run_simul()
            self.player.results.insert(0,self.results)
            try:
                menu.remove_widget('new_results')
                menu.remove_widget('menu_new_results')
            except:
                pass
            
            # MENU AFTER SIMULATION RESULTS
            menu_simul = pygame_menu.Menu(
                height=720,
                onclose=self.toggle_menu,
                theme=mytheme,
                title='New Results',
                width=1280,
                menu_id='menu_new_results'
            )
            
            menu_simul.add.label("Results:")
            menu_simul.add.vertical_margin(50)  # Adds margin
            
            menu.add.button('New Results', action=menu_simul, font_color = 'white', background_color=(0,150,50), button_id='new_results')
            menu_simul.add.label(self.results, label_id='results')
            save_results(self.results)
            save_file([self.player.player_name, self.player.results, self.player.missions_activated, self.player.missions_completed])
            menu_simul.add.vertical_margin(100, margin_id='nr_margin')  # Adds margin
            menu_simul.add.button('Close', pygame_menu.events.BACK, background_color=(70, 70, 70), button_id='nr_close')
           


        def restore_data() -> None:
            """
            """
            menu.reset_value()
            menu_objective.reset_value()
            menu_genes.reset_value()
            menu_reactions.reset_value()
           

        menu.add.dropselect(title='Simulation Method: ',
                            items=[('FBA', 'fba'),
                                   ('pFBA', 'pfba'),
                                #    ('MOMA', 'moma'),
                                   ('lMOMA', 'lmoma'),
                                   ('ROOM','room')],
                                   default=0,
                                   selection_box_height=5, dropselect_id='method')
        menu.add.button('Objective', menu_objective)
        menu.add.button('Genes', menu_genes)
        menu.add.button('Environmental Conditions', menu_reactions)
        menu.add.vertical_margin(50)  # Adds margin
        # menu.add.button('Restore Data', restore_data, background_color=(100,0,0))
        # menu.add.vertical_margin(20)  # Adds margin

        menu.add.button('Run Simulation', action=data_fun, font_color = 'white', background_color=(20,100,100))        
        menu.add.vertical_margin(20)  # Adds margin
        last_results = menu.add.button('Last Results', action=menu_results, font_color = 'white', background_color=(20,0,150))  
        # menu.add.vertical_margin(50)  # Adds margin

        menu.mainloop(self.display_surface)
        


    def toggle_menu(self):
        self.desk_menu = not self.desk_menu




    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK


    def update(self):
        self.input()
        self.setup()

