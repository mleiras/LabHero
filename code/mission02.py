import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save
from button import Button


class Mission02: 
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


        self.menu = Mission02_info(self.toggle_menu, self.player)

    
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):

        self.m02_step1 = [
            f"Greetings {self.player.player_name}!, intrepid explorer of the microbial world! I'm Dr. Silva!",
            "We've compiled a list of ten genes within E. coli, and we suspect that one of them is",
            "essential for its survival. Can you find each one is the essential one to E. coli's?"
        ]
        
        self.m02_step2 = ["Did you already find the essential gene?",
                          "Can you show me your results?"]

        self.m02_step3 = ["Thank you! Your research will unlock a hidden chapter in E. coli's genetic story.",
                          "Your discoveries may have far-reaching implications in our understanding of microbial life."]
        
        self.input()
        if '02' in self.missions_completed:
            self.menu_message(self.m02_step3, buttons=False)

        elif '02' in self.missions_activated:
            self.menu_message(self.m02_step2)

        else:
            self.menu_message(self.m02_step1)

       

    def menu_message(self, message, buttons = True):

        menu_border = pygame.draw.rect(self.screen, (255,215,0), [0,500,1280,220], width=5)
        menu_bg = pygame.draw.rect(self.screen, (186,214,177), [5,505,1270,210])

        # pygame.display.set_caption('Cientista')
        imagem_path = get_resource_path('graphics/dialogues/cientista2.jpg')
        imagem = pygame.image.load(imagem_path).convert()
        
        x = 25; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y))

        cientista_rect = pygame.draw.rect(self.screen, 'white', [25,675,150,25])

        nome = self.font_nome.render('Dr. Silva', True, 'black')
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




class Mission02_info:
    def __init__(self, toggle_menu, player) -> None:

        # general setup
        self.player = player
        self.missions_activated = self.player.missions_activated
        self.missions_completed = self.player.missions_completed

        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path, 30)
        
        self.index = 0
        self.timer = Timer(200)

        if '02' in self.missions_activated:
            self.mission02 = True
        else:
            self.mission02 = False

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
            title='Mission 02',
            width=1280,
        )

        menu_text = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Mission 02 Briefing',
            width=1280
        )

        menu_text.add.label(
            """
            Welcome back, budding scientist! Your journey through the microbial world continues.
            In this mission, you'll unravel the secrets of a crucial gene that's vital for E. coli's survival. Get ready for the Genetic Mystery - The Essential Gene challenge!

            Objective:
            Your primary objective in this mission is to identify the essential gene that E. coli cannot live without.
            Imagine you're solving a microbial puzzle where one missing piece makes all the difference.

            List of possible genes that are essential:
            b1241  b3115  b3736  b2975  b1524  b2278  b2926  b2297  b0728  b3919
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
            Task 1 - The Mystery Genes:
            You'll start with a list of 10 mystery genes, each associated with a specific cellular function. These genes are like keys to E. coli's survival.

            Task 2 - Gene Knockout Simulations:
            Your job is to simulate E. coli's growth without each of these genes, one by one. This process mimics what scientists do in the lab when they "knock out" a gene to observe the consequences.
            
            Task 3 - Observe and Compare:
            As you simulate E. coli's growth without each gene, carefully observe the results. Does the absence of a particular gene affect growth? Do some genes appear more critical than others?
            
            Task 4 - Unravel the Mystery:
            Analyze your observations and deductions. Which gene do you suspect is the essential one? Remember, the essential gene is the one that, when missing, significantly impairs E. coli's growth.
            
            Task 5 - Report Your Findings:
            Compile your findings into a comprehensive report. Explain why you suspect a particular gene is essential and provide evidence from your simulations to support your conclusion.
            
            Hints:
            - Ensure that you simulate with only one gene at a time
            - Identify the gene that stops growth

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )

        
        menu_text.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_text.add.vertical_margin(20)

        menu.add.label("Welcome back, budding scientist! Your journey through the microbial world continues."
            ,wordwrap=False,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=34)
        
        menu.add.label(
            """
            In this mission, you'll unravel the secrets of a crucial gene that's vital for E. coli's survival.
            Get ready for the Genetic Mystery - The Essential Gene challenge!

            List of possible genes that are essential:
            b1241  b3115  b3736  b2975  b1524  b2278  b2926  b2297  b0728  b3919

            """,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=30)
        menu.add.button('Mission 02 Briefing', menu_text, font_color = 'black',background_color=(255,215,0, 255))
        menu.add.vertical_margin(50)  
        if self.mission02:
            menu.add.text_input('Essential Gene: ', default='', input_underline='_', maxchar=5, onreturn=self.deliver_results)
            menu.add.vertical_margin(50)
            menu.add.label('Mission Activated', font_color=(150, 150, 150))
            menu.add.vertical_margin(20)
        else:
            menu.add.button('Activate Mission', action=self.activate_mission02, background_color=(50,100,100))        
        menu.add.vertical_margin(20)  

        menu.mainloop(self.display_surface)



    def toggle_menu(self):
        self.toggle_talk = not self.toggle_talk

    def activate_mission02(self):
        self.mission02 = True
        self.missions_activated.insert(0, '02')
        animation_text_save('Mission 02 Activated')


    def deliver_results(self, ans):
        # print(ans)
        right = self.check_results(ans)

        if right:
            self.success.play()
            self.missions_completed.insert(0, '02')
            animation_text_save('Congratulations! Mission Completed!', time=2000)
        else:
            self.failed.play()
            animation_text_save('No ... Try again!', time=2000)


    def check_results(self, ans):
        if ans == 'b2926':
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
        