import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save
from button import Button


class Mission03: 
    def __init__(self, toggle_menu, player) -> None:
        #general setup 
        self.player = player
        self.missions_activated = self.player.missions_activated
        self.missions_completed = self.player.missions_completed

        self.toggle_menu = toggle_menu

        font_path = get_resource_path('font/LycheeSoda.ttf')

        self.font = pygame.font.Font(font_path,30)
        self.font_nome = pygame.font.Font(font_path,24)
        self.screen = pygame.display.get_surface() 
        self.timer = Timer(200)


        

        self.menu = Mission03_info(self.toggle_menu, self.player)

    
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):

        self.m03_step1 = [
            "I'm Dr. Carter! I'm on a quest to find a replacement for glucose as E. coli's energy source.",
            "I've got a list of potential candidates like malate, lactate, and fructose.",
            "Can you see which one works best?"
        ]
        
        self.m03_step2 = ["Did you already choose the best substitute for glucose?",
                          "Wow ... can you show me your results?"]

        self.m03_step3 = [f"Thank you {self.player.player_name}!",
                          " ",
                          "Finding the right substitute can help in all sorts of science stuff, from making better",
                          "biofuels to cleaning up the environment."
                          ]

        self.input()

        if '03' in self.missions_completed:
            self.menu_message(self.m03_step3, buttons=False)

        elif '03' in self.missions_activated:
            self.menu_message(self.m03_step2)

        else:
            self.menu_message(self.m03_step1)

       

    def menu_message(self, message, buttons = True):

        menu_border = pygame.draw.rect(self.screen, (255,215,0), [0,500,1280,220], width=5)
        menu_bg = pygame.draw.rect(self.screen, (186,214,177), [5,505,1270,210])

        # pygame.display.set_caption('Cientista')
        imagem_path = get_resource_path('graphics/dialogues/carter.jpg')
        imagem = pygame.image.load(imagem_path).convert()
        
        x = 25; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y))

        cientista_rect = pygame.draw.rect(self.screen, 'white', [25,675,150,25])

        nome = self.font_nome.render('Dr. Carter', True, 'black')
        self.screen.blit(nome,(55,677))

        for line, msg in enumerate(message):
            surf = self.font.render(msg, True, 'black')
            self.screen.blit(surf,(200,525+(line*20)+(15*line)))

        if buttons:
            botao_teste = Button(200,650,150,50,self.screen, 'Yes', self.menu.update)
            botao_teste_2 = Button(370,650,220,50,self.screen, 'Not now', self.toggle_menu)
            botao_teste.process()
            botao_teste_2.process()

        pygame.display.flip()




class Mission03_info:
    def __init__(self, toggle_menu, player) -> None:

        # general setup
        self.player = player
        self.missions_activated = self.player.missions_activated
        self.missions_completed = self.player.missions_completed

        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path,30)
        
        self.index = 0
        self.timer = Timer(200)

        if '03' in self.missions_activated:
            self.mission03 = True
        else:
            self.mission03 = False

        #sounds
        success_path = get_resource_path('audio/success_3.wav')
        self.success = pygame.mixer.Sound(success_path)
        self.success.set_volume(1.2)

        failed_path = get_resource_path('audio/failed.wav')
        self.failed = pygame.mixer.Sound(failed_path)
        self.failed.set_volume(1.2)

    def setup(self):
        
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Mission 03',
            width=1280,
        )

        menu_text = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Mission 03 Briefing',
            width=1280
        )

        menu_text.add.label(
            """
            Welcome back, Microbial Explorer! In this mission, we're delving into the world of microbial metabolism once more.
            Our goal is to find a suitable substitute for glucose, E. coli's preferred carbon source.
            If we can identify a good substitute, it could have significant implications for various applications, from biotechnology to environmental science.

            Objective:
            Your mission is to simulate the growth of E. coli using different carbon sources and determine which one serves as the best substitute for glucose.
            We've provided you with a list of potential candidates:
            
            - malate                           - lactate
            - glutamate                        - glutamine
            - fumarate                         - fructose
            - ethanol                          - 2-oxoglutarate
            - acetaldehyde                     - acetate

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_text.add.label(
            """Tasks:""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'gold',
            font_color = 'black',
            font_size = 30,
            padding = (25,25,25,25)
        )
        menu_text.add.label(
            """
            Task 1 - Simulate Growth:
            Use the provided simulation tool to run growth simulations for E. coli using each of the carbon sources listed above.

            Task 2 - Observe Results:
            Pay close attention to the growth patterns and biomass yield for each simulation. Biomass represents the microbial population's growth, and a higher yield indicates better growth.

            Task 3 - Identify the Best Substitute:
            Based on your observations, determine which carbon source serves as the best substitute for glucose in terms of supporting E. coli growth. You can compare the biomass yield of the chosen substitute to that of glucose for reference.

            Why It Matters:
            Understanding which carbon sources E. coli can thrive on is essential for various fields of research and industry. Finding a suitable substitute for glucose can have far-reaching implications, from optimizing bioprocesses to environmental remediation efforts. Your findings could help shape the future of microbiology and biotechnology.

            Scientist's Notes:
            Remember, microbial growth can be influenced by various factors, so it's essential to run multiple simulations and ensure the accuracy of your results. Good luck, Microbial Explorer, and may your discoveries be as sweet as fructose!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )

        
        menu_text.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_text.add.vertical_margin(20)

        menu.add.vertical_margin(20)  
        menu.add.label("""Welcome back, Microbial Explorer! Let's find a suitable substitute for glucose!"""
            ,wordwrap=False,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=34)

        menu.add.label(
            """
            If we can identify a good substitute, it could have significant implications for various applications, from biotechnology to environmental science.

            We've provided you with a list of potential candidates:

            - malate                             - lactate
            - glutamate                        - glutamine
            - fumarate                         - fructose
            - ethanol                            - 2-oxoglutarate
            - acetaldehyde                    - acetate
            """,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=30)
        
        menu.add.button('Mission 03 Briefing', menu_text, font_color = 'black',background_color=(255,215,0, 255))
        menu.add.vertical_margin(50)  
        if self.mission03:
            menu.add.text_input('Substitute: ', default='', input_underline='_', maxchar=14, onreturn=self.deliver_results)
            menu.add.vertical_margin(50)
            menu.add.label('Mission Activated', font_color=(150, 150, 150))
            menu.add.vertical_margin(20)
        else:
            menu.add.button('Activate Mission', action=self.activate_mission03, background_color=(50,100,100))        
        menu.add.vertical_margin(20)  

        menu.mainloop(self.display_surface)



    def toggle_menu(self):
        self.toggle_talk = not self.toggle_talk

    def activate_mission03(self):
        self.mission03 = True
        self.missions_activated.insert(0, '03')
        animation_text_save('Mission 03 Activated')


    def deliver_results(self, ans):
        # print(ans)
        right = self.check_results(ans)

        if right:
            self.success.play()
            self.missions_completed.insert(0, '03')
            animation_text_save('Congratulations! Mission Completed!', time=2000)
        else:
            self.failed.play()
            animation_text_save('No ... Try again!', time=2000)


    def check_results(self, ans):
        if ans == 'fructose':
            return True
        else:
            return False



    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        