import pygame
import pygame_menu
from settings import *
from options_values import *
from save_load import *
from timers import Timer
from functions import animation_text_save



class Menu_2:
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



    def save_game(self, menu):
        name = menu.get_input_data()
        save_file([name, self.player.item_inventory, self.player.seed_inventory, self.player.money])
        animation_text_save('Game saved')
    


    def setup(self):
        menu = pygame_menu.Menu('Lab Hero Settings', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=mytheme)
        

        # menu.add.button('Play', action=pygame_menu.events.BACK) # VER AQUI OUTRA SOLUÇÃO???
        menu.add.text_input('Name: ', default='Margaret Dayhoff', textinput_id='name')
        # menu.add.selector('Difficulty: ', [('Easy', 1), ('Hard', 2)], onchange=self.set_difficulty)
        menu.add.button('Save Game', self.save_game, menu)
        menu.add.button('Quit Game', pygame_menu.events.EXIT)
        menu.mainloop(self.display_surface)


    def toggle_menu(self):
        self.toggle_shop = not self.toggle_shop

    def set_difficulty(value, difficulty):
        # Do the job here !
        pass

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            pygame_menu.events.BACK
            

    def update(self):
        self.input()
        self.setup()
        



    

