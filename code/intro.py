import pygame
from settings import *
import pygame_menu
from options_values import *
from button import Button


class Intro:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 100)
        self.font_text = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.width = 400
        self.space = 10
        self.padding = 8
        self.tutorial = Tutorial()

    def run(self):

        self.display_surface.fill('gold')
        self.title = self.font.render('Lab Hero', False, 'black')
        self.title_rect = self.title.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.display_surface.blit(self.title, self.title_rect)
        self.text = self.font_text.render(
            'press ENTER to continue', False, 'red')  # render(string, AA, color)
        self.text2 = self.font_text.render(
            'or press SPACE to new game', False, (60, 150, 140))  # render(string, AA, color)
        self.text_rect = self.text.get_rect(
            center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+75))
        self.text_rect2 = self.text2.get_rect(
            center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+120))
        self.display_surface.blit(self.text, self.text_rect)
        self.display_surface.blit(self.text2, self.text_rect2)
        # botao_continue = Button(
        #     240, 450, 250, 50, self.display_surface, 'Continue Game', self.continue_game)
        # botao_new = Button(515, 450, 250, 50,
        #                    self.display_surface, 'New Game', self.new_game)
        # botao_tutorial = Button(
        #     790, 500, 250, 50, self.display_surface, 'Tutorial', self.tutorial.update)
        # botao_continue.process()
        # botao_new.process()
        

        botao_tutorial = Button(
            515, 520, 250, 50, self.display_surface, 'Tutorial', self.tutorial.update)
        botao_tutorial.process()



class Tutorial:
    def __init__(self) -> None:

        # genereal setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)


    def setup(self):

        menu_how_to_play = pygame_menu.Menu('How to Play', 1280, 720,
                                            onclose=pygame_menu.events.BACK,
                                            theme=tutorial_theme)

        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Moving""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color=(60, 150, 140),
            font_color='white',
            font_size=30,
            padding=(25, 25, 25, 25)
        )
        menu_how_to_play.add.label(
            """
            Use arrows (up, down, left, righ) or WASD keys to move the character.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Interacting""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color=(60, 150, 140),
            font_color='white',
            font_size=30,
            padding=(25, 25, 25, 25)
        )
        menu_how_to_play.add.label(
            """
            Use ENTER key to open the dialogue when close to another character (scientists).

            Use ENTER key to open the simulation window when close to your desk.

            Use ENTER key to consult books when close to the library.

            Use ENTER key to take an apple from a tree ("An apple a day keeps the doctor away").
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Buttons""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color=(60, 150, 140),
            font_color='white',
            font_size=30,
            padding=(25, 25, 25, 25)
        )
        menu_how_to_play.add.label(
            """
            Use the Mouse to click on the buttons of the dialogues.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Main Menu""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color=(60, 150, 140),
            font_color='white',
            font_size=30,
            padding=(25, 25, 25, 25)
        )
        menu_how_to_play.add.label(
            """
            Use M key to open the Main Menu to control the music/volume, save/exit the game and to see this tutorial again.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)

        menu_how_to_play.mainloop(self.display_surface)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK

    def update(self):
        self.input()
        self.setup()
