import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer

mytheme = pygame_menu.themes.THEME_GREEN.copy()
font = pygame_menu.font.FONT_MUNRO
mytheme.font = font



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


    def save_game(self, name):
        save_file([name, self.player.item_inventory, self.player.seed_inventory, self.player.money])

        sceneExit = False
        time = 1500

        while not sceneExit:

            text_surf = self.font.render(f'Game saved',False,'black')
            text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-20))
            pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10,10),0,2) #ultimos 2 argumentos se quiser bordas redondas pode-se adicionar estes argumentos
            self.display_surface.blit(text_surf, text_rect)

            pygame.display.update()

            passed_time = pygame.time.Clock().tick(60)
            time -= passed_time
            if time <= 0:
                sceneExit = True


    def setup(self):
        menu = pygame_menu.Menu('Lab Hero Settings', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=mytheme)
        

        # menu.add.button('Play', action=pygame_menu.events.BACK) # VER AQUI OUTRA SOLUÇÃO???
        name_menu = menu.add.text_input('Name: ', default='Monica', textinput_id='name')
        name = name_menu.get_value()
        # menu.add.selector('Difficulty: ', [('Easy', 1), ('Hard', 2)], onchange=self.set_difficulty)
        menu.add.button('Save Game', self.save_game, name)
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
        



    

