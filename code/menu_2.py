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
        name = menu.get_input_data()
        save_file([self.player.results, self.player.missions_activated, self.player.missions_completed])
        animation_text_save('Game saved')
    


    def setup(self):
        menu = pygame_menu.Menu('Lab Hero Settings', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=mytheme)
        

        # menu.add.button('Play', action=pygame_menu.events.BACK) # VER AQUI OUTRA SOLUÇÃO???
        menu.add.text_input('Name: ', default='Margaret Dayhoff', textinput_id='name')

        menu.add.selector('Music: ', [('Hope', 0), ('Serene', 1),  ('Happy', 2), ('Surf', 3)], default=self.music_val, onchange=self.set_music)
        menu.add.range_slider('Volume', self.volume*100, (0, 100), 1, onchange=self.set_volume,
                      rangeslider_id='volume_music',
                      value_format=lambda x: str(int(x)))
        # menu.add.progress_bar('Volume', default=100, selectable=True, onselect=self.set_volume)
        menu.add.button('Save Game', self.save_game, menu)
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
        

