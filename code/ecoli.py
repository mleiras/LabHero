import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *


class Ecoli:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path, 30)

        # movement
        self.index = 0
        self.timer = Timer(200)



    def setup(self):
        
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='E. coli',
            width=1280
        )


        menu.add.label(
            'E. coli',
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=50,
            font_color=(70,70,70))
        menu.add.image('graphics/environment/E.coli.png', scale=(1, 1))

        # menu.add.vertical_margin(15)  # Adds margin
        # menu.add.button('How to Play', menu_how_to_play, background_color = (255,215,0, 255)) #aqua»
       # menu.add.vertical_margin(20)  # Adds margin


        menu.mainloop(self.display_surface)

        # return menu


    
    def on_button_click(self, value: str, text = None) -> None:
        if not text:
            print(f'Hello from {value}')
        else:
            print(f'Hello from {text} with {value}')



    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()
            

    def update(self):
        self.input()
        self.setup()
        


