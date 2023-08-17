import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *

mytheme = pygame_menu.themes.THEME_GREEN.copy()
font = pygame_menu.font.FONT_MUNRO
mytheme.font = font


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
            title='Main Menu',
            width=1280
        )


        menu_contributors = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Contributors',
            width=1280
        )

        # Add table to contributors
        table_contrib = menu_contributors.add.table()
        table_contrib.default_cell_padding = 5
        table_contrib.default_row_background_color = 'grey'
        bold_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        table_contrib.add_row(['N°', 'Github User'], cell_font=bold_font)
        for i in range(len(pygame_menu.__contributors__)):
            table_contrib.add_row([i + 1, pygame_menu.__contributors__[i]], cell_font=bold_font if i == 0 else None)

        table_contrib.update_cell_style(-1, -1, font_size=15)  # Update all column/row
        table_contrib.update_cell_style(1, [2, -1], font=pygame_menu.font.FONT_OPEN_SANS_ITALIC)

        menu_text = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Text with scroll',
            width=1280
        )

        menu.add.button('Book 1', menu_text)
        menu.add.button('Book 2', menu_contributors)
        menu.add.vertical_margin(20)  # Adds margin



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
            'id est laborum.',
            max_char=33,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, -1)
        )
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
        


