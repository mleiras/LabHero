import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *


class Books:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)

        # movement
        self.index = 0
        self.timer = Timer(200)



    def setup(self):
        
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Books',
            width=1280
        )


        menu_text = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Book Intro to Modelation',
            width=1280
        )
        

        menu.add.label(
            'Books Available:',
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=50,
            font_color=(70,70,70))
        menu.add.vertical_margin(15)  # Adds margin
        menu.add.button('Systems Biology', menu_text, background_color = 'green')
        menu.add.button('Intro to Modelation', menu_text, background_color = 'blue')
        menu.add.button('How to Simulate', menu_text, background_color = 'red')
        menu.add.button('Do You Know Microorganisms?', menu_text, background_color = 'orange')
        menu.add.button('MEWpy Basics', menu_text, background_color = 'grey')
        menu.add.button('How to Date a Model', menu_text, background_color = 'pink')
        # menu.add.vertical_margin(20)  # Adds margin



        # noinspection SpellCheckingInspection
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
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, -1)
        )
        menu_text.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))


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
        


