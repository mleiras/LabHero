import pygame
import pygame_menu
from settings import *
from level import *
from options_values import *
from save_load import *
from timers import Timer
from functions import animation_text_save



class Menu:
    def __init__(self, player, toggle_menu) -> None:

        # genereal setup
        self.toggle_menu = toggle_menu
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)

        # self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

        #music volume

        self.volume = 0.5
        self.music_val = 0



    def save_game(self, menu):
        self.player.player_name = menu.get_input_data()['name']
        save_file([self.player.player_name, self.player.results, self.player.missions_activated, self.player.missions_completed])
        animation_text_save('Game saved')
    


    def setup(self):
        menu = pygame_menu.Menu('Lab Hero Settings', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=mytheme)
        
        menu_how_to_play = pygame_menu.Menu('How to Play', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=tutorial_theme)
        
        menu_credits = pygame_menu.Menu('Credits', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=mytheme)
        
        # menu_credits.add.label(
        #     """
        #     Font Lychee Soda by jeti {https://fontenddev.com/fonts/lychee-soda/}{link}
        #     Music by 
        #     """,
        #     max_char=-1,
        #     wordwrap=True,
        #     align=pygame_menu.locals.ALIGN_CENTER,
        #     margin=(0, 0)
        # )
        menu_credits.add.vertical_margin(50)
        menu_credits.add.url('https://fontenddev.com/fonts/lychee-soda/', 'Font Lychee Soda by jeti', font_color='firebrick')
        menu_credits.add.vertical_margin(20)
        menu_credits.add.url('https://dafonttop.com/munro.font', 'Font Munro by Ed Merrit', font_color='firebrick')
        menu_credits.add.vertical_margin(20)
        menu_credits.add.url('https://www.FesliyanStudios.com', 'Royalty free music from https://www.FesliyanStudios.com', font_color=(110,175,221))
        menu_credits.add.vertical_margin(20)
        menu_credits.add.url('https://cupnooble.itch.io/', 'Asset Pack by Cup Nooble', font_color=(84,145,76))
        menu_credits.add.vertical_margin(50)
        menu_credits.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_credits.add.vertical_margin(50)
        


        
        
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Moving""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
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
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
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
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
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
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
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
        menu_how_to_play.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))
        menu_how_to_play.add.vertical_margin(50)

        def change_name(teste):
            self.player.player_name = teste
        
        menu.add.text_input('Name: ', default=self.player.player_name, textinput_id='name', onreturn=change_name)
        menu.add.button('How to Play', action=menu_how_to_play)

        menu.add.selector('Music: ', [('Hope', 0), ('Serene', 1),  ('Happy', 2), ('Surf', 3)], default=self.music_val, onchange=self.set_music)
        menu.add.range_slider('Volume', self.volume*100, (0, 100), 1, onchange=self.set_volume,
                      rangeslider_id='volume_music',
                      value_format=lambda x: str(int(x)))
        menu.add.button('Save Game', self.save_game, menu)
        menu.add.button('Credits', action=menu_credits)
        menu.add.button('Quit Game', pygame_menu.events.EXIT)
        menu.mainloop(self.display_surface)

    

    def toggle_menu(self):
        self.toggle_shop = not self.toggle_shop

    def set_music(self, value, extra):
        MUSIC_NAME = value[0][0] # name of music
        self.music_val = value[1] # int value
        self.player.music_bg = pygame.mixer.stop()
        self.player.music_bg = pygame.mixer.Sound(MUSIC[value[0][0]])
        self.player.music_bg.set_volume(self.volume*0.14)
        self.player.music_bg.play(loops = -1)


    def set_volume(self, value):
        self.volume = (value/100)
        self.player.music_bg.set_volume(self.volume*0.14)
        # print(self.volume)
        

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        

