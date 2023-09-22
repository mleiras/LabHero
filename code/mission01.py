import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save
from button import Button

#############################################

class Mission01: # alterar nome classe no caso de usar para todas
    def __init__(self, toggle_menu) -> None:
        self.toggle_menu = toggle_menu

        self.font = pygame.font.Font('../font/LycheeSoda.ttf',34)
        self.font_nome = pygame.font.Font('../font/LycheeSoda.ttf',24)
        self.screen = pygame.display.get_surface() ### set_mode([1280,720])
        self.timer = Timer(200)


        self.mission01 = ["Olá! Tenho uma missão para ti",
                          "Ajuda-me com este modelo de e coli",
                          "Consegues?"]
        self.done = False

        self.menu = Mission_info(self.toggle_menu)

    
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        # if keys[pygame.K_RETURN]:
        #     self.done = True

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.input()
        if not self.done:
            self.menu_message(self.mission01)


    def menu_message(self, message):

        menu_border = pygame.draw.rect(self.screen, 'black', [0,500,1280,220], width=5)
        menu_bg = pygame.draw.rect(self.screen, (186,214,177), [5,505,1270,210])

        # pygame.display.set_caption('Cientista')
        imagem = pygame.image.load("../graphics/dialogues/cientista2.jpg").convert()
        
        x = 20; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y)) 

        nome = self.font_nome.render('Cientista', True, 'black')
        self.screen.blit(nome,(30,690))

        for line, msg in enumerate(message):
            surf = self.font.render(msg, True, 'black')
            self.screen.blit(surf,(220,530+(line*20)+(15*line)))

        botao_teste = Button(220,650,150,50,self.screen, 'Sim', self.menu.update)
        botao_teste_2 = Button(390,650,220,50,self.screen, 'Agora não', self.toggle_menu)
        
        
        botao_teste.process()
        botao_teste_2.process()


        pygame.display.flip()




class Mission_info:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        
        self.index = 0
        self.timer = Timer(200)

        self.mission01 = False #mudar para atributo do player (não aqui) - assim pode-se fazer load game com esta info



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


        # image_path = '../graphics/objects/merchant.png'
        # menu.add.image(image_path, scale=(2,2))
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
            menu.add.button('Deliver Results', action=None, background_color=(50,100,100)) ## TASK: ADICIONAR FUNÇÃO ENTREGAR RESULTADOS  
        else:
            menu.add.button('Activate Mission', action=self.activate_mission01, background_color=(50,100,100))        
        menu.add.vertical_margin(20)  

        menu.mainloop(self.display_surface)



    def toggle_menu(self):
        self.toggle_shop = not self.toggle_shop


    def activate_mission01(self):
        self.mission01 = True
        animation_text_save('Mission 01 Activated')



    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        


