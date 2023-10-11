import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save
from button import Button
from math import isclose


class Mission01: 
    def __init__(self, toggle_menu, player) -> None:
        #general setup 
        self.player = player
        self.missions_activated = self.player.missions_activated
        self.missions_completed = self.player.missions_completed

        self.toggle_menu = toggle_menu

        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        self.font_nome = pygame.font.Font('../font/LycheeSoda.ttf',24)
        self.screen = pygame.display.get_surface() 
        self.timer = Timer(200)


        # self.m01_step1 = [
        #     f"Hello {self.player.player_name}! I'm Dr. Martinez, and I'm working on groundbreaking research involving E. coli.",
        #     "We're trying to understand how this remarkable microbe adapts to different environments,",
        #     "especially anaerobic ones. Can you help me?"
        # ]
        #     # "Olá! Tenho uma missão para ti",
        #     #               "Ajuda-me com este modelo de e coli",
        #     #               "Consegues?"]
        
        # self.m01_step2 = ["Did you already made a simulation?",
        #                   "Can you show me your results?"]

        # self.m01_step3 = ["Thank you! You're pioneering our understanding of E. coli's resilience.",
        #                   "Your discoveries will shape our research."]
        

        self.menu = Mission_info(self.toggle_menu, self.player)

    
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.m01_step1 = [
            f"Hello {self.player.player_name}! I'm Dr. Martinez, and I'm working on groundbreaking research involving E. coli.",
            "We're trying to understand how this remarkable microbe adapts to different environments,",
            "especially anaerobic ones. Can you help me?"
        ]
            # "Olá! Tenho uma missão para ti",
            #               "Ajuda-me com este modelo de e coli",
            #               "Consegues?"]
        
        self.m01_step2 = ["Did you already made a simulation?",
                          "Can you show me your results?"]

        self.m01_step3 = ["Thank you! You're pioneering our understanding of E. coli's resilience.",
                          "Your discoveries will shape our research."]
        

        self.input()
        if '01' in self.missions_completed:
            self.menu_message(self.m01_step3, buttons=False)

        elif '01' in self.missions_activated:
            self.menu_message(self.m01_step2)

        else:
            self.menu_message(self.m01_step1)

       

    def menu_message(self, message, buttons = True):

        menu_border = pygame.draw.rect(self.screen, (255,215,0), [0,500,1280,220], width=5)
        menu_bg = pygame.draw.rect(self.screen, (186,214,177), [5,505,1270,210])

        # pygame.display.set_caption('Cientista')
        imagem = pygame.image.load("../graphics/dialogues/martinez.jpg").convert()
        
        x = 25; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y))

        cientista_rect = pygame.draw.rect(self.screen, 'white', [25,675,150,25])

        nome = self.font_nome.render('Dr. Martinez', True, 'black')
        self.screen.blit(nome,(40,677))

        for line, msg in enumerate(message):
            surf = self.font.render(msg, True, 'black')
            self.screen.blit(surf,(200,525+(line*20)+(15*line)))

        if buttons:
            botao_teste = Button(200,650,150,50,self.screen, 'Yes', self.menu.update)
            botao_teste_2 = Button(370,650,220,50,self.screen, 'Not now', self.toggle_menu)
            botao_teste.process()
            botao_teste_2.process()

        pygame.display.flip()




class Mission_info:
    def __init__(self, toggle_menu, player) -> None:

        # general setup
        self.player = player
        self.missions_activated = self.player.missions_activated
        self.missions_completed = self.player.missions_completed

        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        
        self.index = 0
        self.timer = Timer(200)

        if '01' in self.missions_activated:
            self.mission01 = True
        else:
            self.mission01 = False

        #sounds     
        self.success = pygame.mixer.Sound('../audio/success_3.wav')
        self.success.set_volume(1.2)

        self.failed = pygame.mixer.Sound('../audio/failed.wav')
        self.failed.set_volume(1.2)


    def setup(self):
        
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Mission 01',
            width=1280,
        )

        menu_text = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Mission 01 Briefing',
            width=1280
        )


        menu_text.add.label(
            "\n"
            "For this initial mission, we have chosen Flux Balance Analysis (FBA) as "
            "the simulation method for several important reasons: \n\n"
            "- Fundamental Understanding: FBA provides a foundational understanding of "
            "how metabolic networks function. It's an excellent starting point for exploring "
            "the intricacies of E. coli's metabolism.\n\n"
            "- Anaerobic Adaptations: FBA allows you to analyze E. coli's metabolic "
            "reactions and predict how they adapt to anaerobic conditions. This is "
            "crucial as anaerobic environments often require different metabolic strategies. \n"
            "Steady-State Analysis: FBA focuses on achieving a metabolic steady state, which "
            "is essential for understanding how E. coli balances its reactions to grow and "
            "thrive under specific conditions.\n\n"
            "- Comparative Analysis: FBA enables you to compare anaerobic simulations with later "
            " missions involving other methods like pFBA, lMOMA, and ROOM. This comparison will "
            " highlight the advantages and limitations of each method.\n"
            "\n"
            "Hints:\n"
            "- Ensure the absence of oxygen in your simulation. "
            # "- Familiarize yourself with the basics of FBA, such as setting objectives and constraints."
            # "- Analyze the predicted flux distributions to understand which metabolic pathways are"
            # " active in anaerobic conditions."
            ,
            max_char=33,
            wordwrap=True
        )
        menu_text.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))

        menu.add.label('Welcome, Lab Hero! \nYour journey begins with Mission 01: Into the Microbial World.\n'
            ,wordwrap=False,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=34)
        
        menu.add.label(
            "In this mission, you will step into the fascinating world of E. coli, a microscopic organism with incredible metabolic abilities.\n"
            "Your goal is to simulate and observe E. coli's behavior under anaerobic conditions.\n" 
            "Anaerobic means 'without oxygen', and it's time to uncover the secrets of how E. coli thrives in these challenging environments.",
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=30)
        menu.add.button('Mission 01 Briefing', menu_text, font_color = 'black',background_color=(255,215,0, 255))
        menu.add.vertical_margin(50)  
        if self.mission01:
            menu.add.label('Mission Activated', font_color=(150, 150, 150))
            menu.add.vertical_margin(20)  
            menu.add.button('Deliver Results', action=self.deliver_results, background_color=(50,100,100)) ## TASK: ADICIONAR FUNÇÃO ENTREGAR RESULTADOS  
        else:
            menu.add.button('Activate Mission', action=self.activate_mission01, background_color=(50,100,100))        
        menu.add.vertical_margin(20)  

        menu.mainloop(self.display_surface)



    def toggle_menu(self):
        self.toggle_talk = not self.toggle_talk


    def activate_mission01(self):
        self.mission01 = True
        self.missions_activated.insert(0, '01')
        animation_text_save('Mission 01 Activated')


    def deliver_results(self):
        right = self.check_results()

        if right:
            self.success.play()
            self.missions_completed.insert(0, '01')
            animation_text_save('Congratulations! Mission Completed!', time=2000)
            # self.success.play()
        else:
            self.failed.play()
            animation_text_save('No ... Try again!', time=2000)


    def check_results(self):
        # try:
        #     # res = load_file('data')[0]
        #     res = load_file('player_history/results')
        #     # print(str(res))
        #     # print(res2)

        #     menu_results.add.label(res)
        # except:
        #     menu_results.add.label('You have to make at least one simulation to see results.')
        m01_results = load_file('player_history/mission01') 
        try:
            name, *data = load_file('player_history/data')
            results = data[0][0]

            value = float(results[11:21])
            right_value = float(m01_results[11:21])
            
            if isclose(value, right_value, abs_tol=10**-8): 
                return True
            else:
                return False
        except:
            return False


    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        