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

        self.font = pygame.font.Font('../font/LycheeSoda.ttf',34)
        self.font_nome = pygame.font.Font('../font/LycheeSoda.ttf',24)
        self.screen = pygame.display.get_surface() 
        self.timer = Timer(200)


        self.m01_step1 = ["Olá! Tenho uma missão para ti",
                          "Ajuda-me com este modelo de e coli",
                          "Consegues?"]
        
        self.m01_step2 = ["Queres entregar os resultados?"]

        self.m01_step3 = ["Obrigada pela tua ajuda!"]
        

        self.menu = Mission_info(self.toggle_menu, self.player)

    
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
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
        imagem = pygame.image.load("../graphics/dialogues/cientista2.jpg").convert()
        
        x = 25; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y))

        cientista_rect = pygame.draw.rect(self.screen, 'white', [25,675,150,25])

        nome = self.font_nome.render('Cientista', True, 'black')
        self.screen.blit(nome,(55,677))

        for line, msg in enumerate(message):
            surf = self.font.render(msg, True, 'black')
            self.screen.blit(surf,(200,525+(line*20)+(15*line)))

        if buttons:
            botao_teste = Button(200,650,150,50,self.screen, 'Sim', self.menu.update)
            botao_teste_2 = Button(370,650,220,50,self.screen, 'Agora não', self.toggle_menu)
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


    def setup(self):
        
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Mission 1',
            width=1280,
        )

        menu_text = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='About Mission 01',
            width=1280
        )


        menu_text.add.label(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
            'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
            'id est laborum.'
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
            'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
            'id est laborum.'
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
            'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
            'id est laborum.'
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
            'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
            'id est laborum.'
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
            'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
            'id est laborum.',
            max_char=33,
            wordwrap=True
        )
        menu_text.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))

        menu.add.label(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.'

            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea ',
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=30)
        menu.add.button('More Details', menu_text)
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
        self.toggle_shop = not self.toggle_shop


    def activate_mission01(self):
        self.mission01 = True
        self.missions_activated.insert(0, '01')
        animation_text_save('Mission 01 Activated')


    def deliver_results(self):
        right = self.check_results()

        if right:
            self.missions_completed.insert(0, '01')
            animation_text_save('Congratulations! Mission Completed!')
        else:
            animation_text_save('No... Try again!')


    def check_results(self):
        m01_results = load_file('mission01') 
        data = load_file('player_history/data')
        results = data[0][0]

        value = float(results[11:21])
        right_value = float(m01_results[11:21])
        
        if isclose(value, right_value, abs_tol=10**-8): 
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
        

