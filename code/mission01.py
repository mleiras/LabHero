import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save



class Mission01:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        
        self.index = 0
        self.timer = Timer(200)


        self.mission01 = False # mudar com o load game



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
        


        image_path = '../graphics/objects/merchant.png'
        menu.add.image(image_path, scale=(2,2))
        menu.add.label(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.'

            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea ',
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=30)
        menu.add.button('More Info', menu_text)
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
        


