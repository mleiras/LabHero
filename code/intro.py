import pygame
from settings import *
import pygame_menu
from options_values import *
from button import Button
from utils import *


class Intro:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path, 130)
        self.font_text = pygame.font.Font(font_path, 30)
        self.width = 400
        self.space = 10
        self.padding = 8
        self.controls = Tutorial()
        self.story = Story()

    def run(self):

        self.display_surface.fill('gold')
        self.title = self.font.render('Lab Hero', False, 'black')
        self.title_rect = self.title.get_rect(
            center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)-100))
        self.display_surface.blit(self.title, self.title_rect)
        self.text = self.font_text.render(
            'press ENTER to continue', False, 'red')  # render(string, AA, color)
        self.text2 = self.font_text.render(
            'or press SPACE to new game', False, (60, 150, 140))  # render(string, AA, color)
        self.text_rect = self.text.get_rect(
            center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)))
        self.text_rect2 = self.text2.get_rect(
            center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+40))
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
            515, 450, 250, 50, self.display_surface, 'Controls', self.controls.update, bg_color= 'black', font_color='white')
        botao_tutorial.process()

        botao_story = Button(
            515, 510, 250, 50, self.display_surface, 'Story', self.story.update)
        botao_story.process()



class Tutorial:
    def __init__(self) -> None:

        # genereal setup
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path, 30)


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
            Use ENTER key to open the dialogue when close to another character.

            Use ESCAPE key to close the dialogue with another character.

            Use ENTER key to open the simulation window when close to your desk.

            Use ENTER key to consult books when close to the library.

            Use ENTER key to take an apple from a tree, because why not?
            
            Use ENTER key to try some coffee and see if it has some effect on you.
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
            Use the Mouse to click on the buttons of the dialogues or menus.
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


class Story:
    def __init__(self) -> None:

        # genereal setup
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path, 30)


    def setup(self):

        menu_story = pygame_menu.Menu('LabHero Story', 1280, 720,
                                            onclose=pygame_menu.events.BACK,
                                            theme=tutorial_theme)
        menu_story.add.label(
            """
            You’re a bioinformatician working at the University.
            
            You have a desk in the office of the Bioinformatics Department, where you can chat and socialize with your fellow bioinformaticians about the various projects they work on.
            
            Your job is to help fellow researchers with the various problems they encounter during their projects. In the labs, you’ll find various missions in the field of systems biology and metabolic modeling. To complete these missions you’ll need to talk to the researchers and understand the challenges they face.
            
            You will quickly find yourself having to carry out simulations with different environmental and genetic conditions, as suggested by the researchers, in order to obtain results more quickly.
            
            You can also study and learn more about systems biology and metabolic modeling with books you’ll find in your office library to help you complete the missions.
            
            Welcome to LabHero!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            padding = (50,50)
        )
        
        menu_story.mainloop(self.display_surface)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK

    def update(self):
        self.input()
        self.setup()
